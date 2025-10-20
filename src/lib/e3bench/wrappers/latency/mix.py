import csv
from pathlib import Path
from typing import Union
from loguru import logger
import time
import shlex
import subprocess
import signal
import sys
import numpy as np


# Try to import torch.benchmark (optional)
try:
    import torch.utils.benchmark as torch_bench
except Exception:
    torch_bench = None

_stop_requested = False


def handle_sigint(sig, frame):
    global _stop_requested
    logger.warning("Ctrl+C pressed — finishing current run and stopping...")
    _stop_requested = True


def mix_latency_wrap_prog(prog_command: str, output_path: Union[str, Path], min_ms=100, warmup=0, repeat=1):
    logger.info(f"[STARTED] Recording latency")
    _start_ns = time.time_ns()

    if not torch_bench:
        logger.error("torch.utils.benchmark is not available. Please install PyTorch.")
        sys.exit(1)
    
    # Register SIGINT handler
    signal.signal(signal.SIGINT, handle_sigint)
    
    # Parse the command string into a list for subprocess
    cmd = shlex.split(prog_command)

    total_runs = warmup + repeat
    logger.debug(f"Running command: {prog_command}")
    logger.debug(f"Warmup: {warmup}  |  Measured: {repeat}  |  Total: {total_runs}\n")

    def fn():
        subprocess.run(cmd).returncode

    # Timer that calls fn() once per iteration
    t = torch_bench.Timer(stmt="fn()", globals={"fn": fn})

    # Prefer adaptive_autorange if available; else fallback to blocked_autorange
    autorange = getattr(t, "adaptive_autorange", None)
    if autorange is None:
        autorange = t.blocked_autorange
    
    # Prepare CSV
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "run_idx", "warmup", "repeat", "min_ms", "timestamp_ns", "duration_ns", 
        "nb_iter", "nb_per_run", "duration__mean__ns", "duration__median__ns",
        "duration__std__ns", "duration__iqr__ns", "returncode"]

    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(total_runs):
            row = {}
            if _stop_requested:
                break

            try:
                start_ns = time.time_ns()
                measure = autorange(min_run_time=min_ms/1000)
                end_ns = time.time_ns()
                duration_ns = end_ns - start_ns

                nb_iter = len(measure.raw_times)
                nb_per_run = measure.number_per_run
                dt_mean = measure.mean * 1e9
                dt_std = np.std(measure.raw_times) * 1e9
                dt_median = measure.median * 1e9
                dt_iqr = measure.iqr * 1e9

                row = {
                    "run_idx": i,
                    "warmup": warmup,
                    "repeat": repeat,
                    "min_ms": min_ms,
                    "nb_iter": nb_iter,
                    "nb_per_run": nb_per_run,
                    "timestamp_ns": start_ns,
                    "duration_ns": duration_ns,
                    "duration__mean__ns": dt_mean,
                    "duration__median__ns": dt_median,
                    "duration__std__ns": float(dt_std),
                    "duration__iqr__ns": dt_iqr,
                    "returncode": 0,
                }

                logger.info(f"[Run {i:02d}] start_ns={start_ns} end_ns={end_ns} "
                f"duration_ms={duration_ns*1e-6:.3f} returncode={0}")
            except KeyboardInterrupt:
                # User interrupted during child run
                end_ns = time.time_ns()
                row = {
                    "run_idx": i,
                    "warmup": warmup,
                    "repeat": repeat,
                    "min_ms": min_ms,
                    "returncode": -130,  # conventional code for SIGINT
                }
            except Exception as e:
                row = {
                    "run_idx": i,
                    "warmup": warmup,
                    "repeat": repeat,
                    "min_ms": min_ms,
                    "returncode": -1,
                }
                logger.error(f"Command failed: {e}")

            writer.writerow(row)
            f.flush()  # ensure row is written promptly

    time.sleep(0.01)
    
    _end_ns = time.time_ns()
    logger.info(f"[FINISHED] Recording latency. Took {(_end_ns - _start_ns)*1e-6:.3f} milliseconds")

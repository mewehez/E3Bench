import csv
from pathlib import Path
from typing import Union
from loguru import logger
import time
import shlex
import subprocess
import signal
import sys


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


def dynamic_latency_wrap_prog(prog_command: str, output_path: Union[str, Path], min_ms=100):
    logger.info(f"[STARTED] Recording latency")
    _start_ns = time.time_ns()

    if not torch_bench:
        logger.error("torch.utils.benchmark is not available. Please install PyTorch.")
        sys.exit(1)
    
    # Register SIGINT handler
    signal.signal(signal.SIGINT, handle_sigint)
    
    # Parse the command string into a list for subprocess
    cmd = shlex.split(prog_command)

    logger.debug(f"Running command: {prog_command}")

    # Storage for per-run records and a counter (no class; use closure)
    records = []
    run_idx = 0

    def fn():
        nonlocal run_idx
        try:
            start_ns = time.time_ns()
            result = subprocess.run(cmd)
            end_ns = time.time_ns()
            duration_ns = end_ns - start_ns
            rc = result.returncode

            records.append({
                "run_idx": run_idx,
                "min_ms": min_ms,
                "timestamp_ns": start_ns,
                "duration_ns": duration_ns,
                "returncode": rc,
            })
            logger.debug(f"[Run {run_idx:03d}] ts={start_ns} ns  dur={duration_ns} ns  rc={rc}")
            run_idx += 1
        except KeyboardInterrupt:
            # User interrupted during child run
            end_ns = time.time_ns()
            records.append({
                "run_idx": run_idx,
                "min_ms": min_ms,
                "returncode": -130,  # conventional code for SIGINT
            })
            run_idx += 1
            raise
        except Exception:
            records.append({
                "run_idx": run_idx,
                "min_ms": min_ms,
                "returncode": -1,
            })
            run_idx += 1
        
        # If Ctrl+C was pressed between runs, stop after recording this run
        if _stop_requested:
            raise KeyboardInterrupt


    # Timer that calls fn() once per iteration
    t = torch_bench.Timer(stmt="fn()", globals={"fn": fn})

    # Choose autorange variant
    autorange = getattr(t, "adaptive_autorange", None) or t.blocked_autorange

    try:
        autorange(min_run_time=min_ms/1000)
    except KeyboardInterrupt:
        logger.warning("Interrupted -- writing partial results...")

    # Write CSV
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["run_idx", "min_ms", "timestamp_ns", "duration_ns", "returncode"])
        writer.writeheader()
        writer.writerows(records)
    
    time.sleep(0.01)
    _end_ns = time.time_ns()
    logger.info(f"[FINISHED] Recording latency. Took {(_end_ns - _start_ns)*1e-6:.3f} milliseconds")

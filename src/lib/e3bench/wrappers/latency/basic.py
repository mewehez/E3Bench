import csv
from pathlib import Path
from typing import Union
from loguru import logger
import time
import shlex
import subprocess
import signal


_stop_requested = False


def handle_sigint(sig, frame):
    global _stop_requested
    logger.warning("Ctrl+C pressed — finishing current run and stopping...")
    _stop_requested = True


def basic_latency_wrap_prog(prog_command: str, output_path: Union[str, Path], warmup=0, repeat=1):
    logger.info(f"[STARTED] Recording latency")
    _start_ns = time.time_ns()

    # Register Ctrl+C handler
    signal.signal(signal.SIGINT, handle_sigint)

    # Parse the command string into a list for subprocess
    cmd = shlex.split(prog_command)
    total_runs = warmup + repeat

    logger.debug(f"Running command: {prog_command}")
    logger.debug(f"Warmup: {warmup}  |  Measured: {repeat}  |  Total: {total_runs}\n")

    # Prepare CSV
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["run_idx", "warmup", "repeat", "timestamp_ns", "duration_ns", "returncode"]

    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(total_runs):
            row = {}
            if _stop_requested:
                break

            try:
                start_ns = time.time_ns()
                result = subprocess.run(cmd)
                end_ns = time.time_ns()
                duration_ns = end_ns - start_ns
                rc = result.returncode
                row = {
                    "run_idx": i,
                    "warmup": warmup,
                    "repeat": repeat,
                    "timestamp_ns": start_ns,
                    "duration_ns": duration_ns,
                    "returncode": rc,
                }
                logger.info(f"[Run {i:02d}] start_ns={start_ns} end_ns={end_ns} "
                f"duration_ms={duration_ns*1e-6:.3f} returncode={rc}")
            except KeyboardInterrupt:
                # User interrupted during child run
                end_ns = time.time_ns()
                row = {
                    "run_idx": i,
                    "warmup": warmup,
                    "repeat": repeat,
                    "returncode": -130,  # conventional code for SIGINT
                }
            except Exception as e:
                row = {
                    "run_idx": i,
                    "warmup": warmup,
                    "repeat": repeat,
                    "returncode": -1,
                }
                logger.error(f"Command failed: {e}")

            writer.writerow(row)
            f.flush()  # ensure row is written promptly
    
    time.sleep(0.01)
    _end_ns = time.time_ns()
    logger.info(f"[FINISHED] Recording latency. Took {(_end_ns - _start_ns)*1e-6:.3f} milliseconds")


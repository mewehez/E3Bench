import shlex
import subprocess
import signal
import os
import time
from loguru import logger

from e3bench.utils import profiler_path_from_name


def send_interrupt(proc: subprocess.Popen):
    try:
        # send SIGINT to the whole group
        if proc.poll() is None:
            os.killpg(os.getpgid(proc.pid), signal.SIGINT)
    except Exception:
        # Fallback: try SIGINT directly (POSIX) / ignore if unsupported
        try:
            if proc.poll() is None:
                proc.send_signal(signal.SIGINT)
        except Exception:
            pass


def force_kill(proc: subprocess.Popen):
    try:
        # Always also call .kill() to ensure the process object is reaped
        if proc.poll() is None:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            proc.kill()
    except Exception:
        try:
            if proc.poll() is None:
                proc.kill()
        except Exception:
            pass


def basic_power_wrap_prog(profiler_name, interval, prog_command, output_path, grace_seconds=2):
    logger.info(f"[STARTED] Recording power")
    _start_ns = time.time_ns()

    # Define power profiler program
    power_profiler = profiler_path_from_name(profiler_name)
    profiler_prog = f"{power_profiler} {interval} {output_path}"

    # Start power profiler in the background
    logger.info(f"Starting power profiler (background): {profiler_prog}")
    # new session so we can signal the whole group
    profiler_proc = subprocess.Popen(
        shlex.split(profiler_prog),
        shell=False,
        preexec_fn=os.setsid,   # new process group/session
    )

    time.sleep(4)

    # Start main programn in the main thread
    logger.info(f"Running main program (foreground): {prog_command}")
    try:
        result = subprocess.run(shlex.split(prog_command), shell=False)
        rc1 = result.returncode
    except KeyboardInterrupt:
        # Already handled by on_sigint, but guard just in case
        rc1 = -130
    except Exception as e:
        rc1 = -1
        logger.error(f"An error occurred: {e}")

    time.sleep(2)
    
    logger.info(f"main program exited with code {rc1}. Stopping power profiler...")
    send_interrupt(profiler_proc)

    # Wait for graceful shutdown of profiler
    try:
        profiler_proc.wait(timeout=grace_seconds)
        logger.info("power profiler stopped gracefully.")
    except subprocess.TimeoutExpired:
        logger.warning("power profiler did not stop after SIGINT; force-killing.")
        force_kill(profiler_proc)
        try:
            profiler_proc.wait(timeout=1.0)
        except Exception:
            pass

    time.sleep(0.01)
    _end_ns = time.time_ns()
    logger.info(f"[FINISHED] Recording power. Took {(_end_ns - _start_ns)*1e-6:.3f} milliseconds")

    # Forward main program's return code
    return rc1

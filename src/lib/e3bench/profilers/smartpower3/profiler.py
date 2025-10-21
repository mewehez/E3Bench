from argparse import ArgumentParser, Namespace
import time
from loguru import logger
from pathlib import Path

try:
    import serial
except Exception as e:
    logger.error("pyserial is not installed. Install with: pip install pyserial")
    raise


def get_args() -> Namespace:
    p = ArgumentParser(description="Read lines from a serial port at a fixed interval and log to file.")
    p.add_argument("--port", required=True, help="Serial port (e.g. COM5")
    p.add_argument("--interval", type=float, required=True, help="Interval between reads in milliseconds")
    p.add_argument("--output-path", required=True, type=Path, help="Output file path")
    p.add_argument("--baudrate", type=int, default=921600, help="Baud rate (default: 921600)")
    p.add_argument("--timeout", type=float, default=0.0, help="Serial read timeout in seconds (default: 0)")
    return p.parse_args()


def main(args: Namespace):
    args = get_args()

    wait_s = max(0.0, args.interval_ms / 1000.0)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    # Open serial
    ser = serial.Serial(
        port=args.port,
        baudrate=args.baudrate,
        bytesize=8,
        parity=serial.PARITY_NONE,
        rtscts=True,
        timeout=args.timeout,
    )

    if not ser.is_open:
        ser.open()

    logger.debug(f"Reading {args.port} @ {args.baudrate} baud. Interval={args.interval} ms --> {args.out_path}")
    logger.info("Press Ctrl+C to stop.")

    # Create or truncate output file and write a CSV header
    f = args.out.open("w", buffering=1, encoding="utf-8")
    header = (
        "timestamp_ns,time,"
        "voltage_in,current_in,power_in,on_off_in,"
        "voltage_c0,current_c0,power_c0,on_off_c0,interrupts_c0,"
        "voltage_c1,current_c1,power_c1,on_off_c1,interrupts_c1"
    )
    f.write(f"{header}\n")

    lines_written = 0
    t_next = time.monotonic()

    try:
        while True:
            start_ns = time.time_ns()
            raw = ser.readline()  # reads until '\n' or timeout
            if raw:
                # Decode safely; replace undecodable bytes
                line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
                f.write(f"{start_ns},{line}\n")
                lines_written += 1

            # Sleep until next tick (fixed-rate scheduling)
            t_next += wait_s
            now = time.monotonic()
            delay = t_next - now
            if delay > 0:
                time.sleep(delay)
            else:
                # We're behind schedule; catch up next iteration
                t_next = now
    except KeyboardInterrupt:
        print("\n[INFO] Ctrl+C received. Stopping...")
    finally:
        try:
            f.flush()
            f.close()
        except Exception:
            pass
        try:
            ser.close()
        except Exception:
            pass
        print(f"[INFO] Closed serial and file. Lines written: {lines_written}")


if __name__ == "__main__":
    args = get_args()
    main(args)

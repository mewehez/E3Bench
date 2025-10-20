from argparse import Namespace, ArgumentParser
import time


def get_args() -> Namespace:
    parser = ArgumentParser(description="Sleep for a given number of milliseconds.")
    parser.add_argument("--ms", type=float, required=True, help="Time to wait (in milliseconds)")

    return parser.parse_args()
    


def wait_for_sec(args: Namespace):
    wait_s = args.ms / 1000.0
    start_ns = time.time_ns()
    time.sleep(wait_s)
    end_ns = time.time_ns()

    print("----"*20)
    print(f"Slept for {args.ms} ms ({wait_s:.3f} s)")
    print(f"Start (ns): {start_ns}")
    print(f"End   (ns): {end_ns}")
    print(f"Measured duration (ms): {(end_ns - start_ns)*1e-6}")
    print("----"*20)


if __name__ == "__main__":
    args = get_args()
    wait_for_sec(args)

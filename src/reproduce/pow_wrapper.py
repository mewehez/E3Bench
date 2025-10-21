from argparse import ArgumentParser, Namespace

# Import local lib
import sys
from pathlib import Path

lib_dir = (Path(__file__).parent / "../lib").resolve()
lib_dir = str(lib_dir)
# Add to sys.path if not already there
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

from e3bench.wrappers import basic_power_wrap_prog


def get_args() -> Namespace:
    parser = ArgumentParser(description="Run a command once and log start/end times.")

    parser.add_argument("--prog", required=True,
        help="Program command to run (quote if it has spaces). Example: --prog 'python3 myscript.py'")
    parser.add_argument("--profiler-name", type=str, required=True,
                        help="The name of the power profiler. Example: tegrastats")
    parser.add_argument("--interval", type=int, default=100,
                        help="Minimum milliseconds between two samples.")
    parser.add_argument("--output-path", required=True, type=Path,
                        help="Output text file path")
    
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    basic_power_wrap_prog(args.profiler_name, args.interval, args.prog, args.output_path)
    


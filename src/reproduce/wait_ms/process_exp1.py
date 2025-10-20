import glob
import re
from pathlib import Path
from loguru import logger
import pandas as pd
import csv

THIS_DIR = Path(__file__).parent.resolve() 

CONFIG_RE = re.compile(r'w(?P<warmup>\d+)_r(?P<repeat>\d+)_ms(?P<ms>\d+)')


if __name__ == "__main__":
    output_dir = (THIS_DIR / "../../../outputs").resolve()
    path_regex = str(output_dir/"wait_ms/measurability/lat_wrapper/*-latency.csv")
    files = glob.glob(path_regex)

    # Prepare CSV
    output_path = output_dir / "wait_ms/measurability/lat_wrapper.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["warmup", "repeat", "ms", "duration_ns", "duration__std_ns", "duration__iqr_ns"]

    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for file_path in files:
            file_path = Path(file_path)

            if m := CONFIG_RE.search(file_path.stem):
                logger.debug(f"Processing {file_path}")
                warmup = int(m.group('warmup'))
                repeat = int(m.group('repeat'))
                ms = int(m.group('ms'))

                df = pd.read_csv(file_path)
                df = df[(df["run_idx"] >= warmup) & (df["returncode"] == 0)]

                duration_ns = df["duration_ns"].median()
                duration__std_ns = df["duration_ns"].std()
                q1 = df["duration_ns"].quantile(0.25)
                q3 = df["duration_ns"].quantile(0.75)
                duration__iqr_ns = q3-q1

                logger.debug(f"Duration: {duration_ns} | Stdev: {duration__std_ns}")

                writer.writerow({
                    "warmup": warmup,
                    "repeat": repeat,
                    "ms": ms,
                    "duration_ns": duration_ns,
                    "duration__std_ns": duration__std_ns,
                    "duration__iqr_ns": duration__iqr_ns,
                })
                f.flush()


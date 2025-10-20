import glob
import re
from pathlib import Path
from loguru import logger
import pandas as pd
import csv

THIS_DIR = Path(__file__).parent.resolve() 

CONFIG_RE = re.compile(r'm(?P<min_ms>\d+)_ms(?P<ms>\d+)')


if __name__ == "__main__":
    output_dir = (THIS_DIR / "../../../outputs").resolve()
    path_regex = str(output_dir/"wait_ms/measurability/dyn_lat_wrapper/*-latency.csv")
    files = glob.glob(path_regex)

    # Prepare CSV
    output_path = output_dir / "wait_ms/measurability/dyn_lat_wrapper.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["repeat", "min_ms", "ms", "duration_ns", "duration__std_ns", "duration__iqr_ns"]

    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for file_path in files:
            file_path = Path(file_path)

            if m := CONFIG_RE.search(file_path.stem):
                logger.debug(f"Processing {file_path}")
                min_ms = int(m.group('min_ms'))
                ms = int(m.group('ms'))

                df = pd.read_csv(file_path)
                repeat = df.shape[0]

                duration_ns = df["duration_ns"].median()
                duration__std_ns = df["duration_ns"].std()
                q1 = df["duration_ns"].quantile(0.25)
                q3 = df["duration_ns"].quantile(0.75)
                duration__iqr_ns = q3-q1

                logger.debug(f"Duration: {duration_ns} | Stdev: {duration__std_ns}")

                writer.writerow({
                    "repeat": repeat,
                    "min_ms": min_ms,
                    "ms": ms,
                    "duration_ns": duration_ns,
                    "duration__std_ns": duration__std_ns,
                    "duration__iqr_ns": duration__iqr_ns,
                })
                f.flush()


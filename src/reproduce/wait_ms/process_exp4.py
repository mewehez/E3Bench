import glob
from pathlib import Path
from loguru import logger
import sys
import pandas as pd


lib_dir = (Path(__file__).parent / "../../lib").resolve()
lib_dir = str(lib_dir)
# Add to sys.path if not already there
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

from e3bench.profilers.tegrastats import post_process_tegra_jon

THIS_DIR = Path(__file__).parent.resolve() 


if __name__ == "__main__":
    output_dir = (THIS_DIR / "../../../outputs").resolve()
    path_regex = str(output_dir/"wait_ms/measurability/pow_wrapper/*/*-power.txt")
    files = glob.glob(path_regex)

    for file_path in files:
        file_path = Path(file_path)
        profiler_name = file_path.parts[-2]
        df = None
        if profiler_name.startswith("inaprof"):
            df = pd.read_csv(file_path)
            df = df.rename(columns={"timestamp": "timestamp_ns", "current": "cur_ma", "voltage": "vol_mv"})
            df["power_mw"] = df["cur_ma"] * df["vol_mv"] * 1e-3
        elif profiler_name == "tegrastats":
            df = post_process_tegra_jon(file_path)

        if df is not None:
            out_path = file_path.parent / f"{file_path.stem}.csv"
            df.to_csv(out_path, index=False)
            logger.debug(f'Parsed {len(df)} rows -> {out_path}')

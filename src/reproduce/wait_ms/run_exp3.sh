#!/bin/bash

set -euo pipefail

WARMUP=5
WAIT_MS=(5000 1000 500 200 100 50 10 1)
MIN_MS=(5 100 1000)
REPEAT=30
PYTHON="python3"

# Resolved path of the directory where this file lives
THIS_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
prog_path="${THIS_DIR}/prog.py"
wrapper_path="${THIS_DIR}/../mix_lat_wrapper.py"
output_dir="${THIS_DIR}/../../../outputs/wait_ms/measurability/mix_lat_wrapper"

# Sanity checks
[ -f "$prog_path" ] || { echo "ERROR: Program not found: $prog_path"; exit 1; }
[ -f "$wrapper_path" ] || { echo "ERROR: Wrapper not found: $wrapper_path"; exit 1; }
mkdir -p "$output_dir"

# Loop through WAIT_MS and REPEAT
for ms in "${WAIT_MS[@]}"; do
  for min_ms in "${MIN_MS[@]}"; do
    output_name="w${WARMUP}_r${REPEAT}_m${min_ms}_ms${ms}"
    out_csv="${output_dir}/${output_name}-latency.csv"

    prog_command="${PYTHON} ${prog_path} --ms ${ms}"

    echo "[INFO] Running: ${output_name}"
    echo "       Command: ${prog_command}"
    echo "       Output : ${out_csv}"

    "${PYTHON}" "${wrapper_path}" \
      --prog "${prog_command}" \
      --warmup "${WARMUP}" \
      --repeat "${REPEAT}" \
      --min-ms "${min_ms}" \
      --output-path "${out_csv}"

    echo "[DONE] ${output_name}"
    echo
  done
done

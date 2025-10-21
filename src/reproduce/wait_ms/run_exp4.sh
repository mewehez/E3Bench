#!/bin/bash

set -euo pipefail

WAIT_MS=5000
INTERVAL=10
PROF_NAME=tegrastats #inaprof-vdd_in
SUFFIX=power.csv
PYTHON="python3"

# Resolved path of the directory where this file lives
THIS_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
prog_path="${THIS_DIR}/prog.py"
wrapper_path="${THIS_DIR}/../pow_wrapper.py"
output_dir="${THIS_DIR}/../../../outputs/wait_ms/measurability/pow_wrapper/${PROF_NAME}"

# Sanity checks
[ -f "$prog_path" ] || { echo "ERROR: Program not found: $prog_path"; exit 1; }
[ -f "$wrapper_path" ] || { echo "ERROR: Wrapper not found: $wrapper_path"; exit 1; }
mkdir -p "$output_dir"


output_name="i${INTERVAL}_ms${WAIT_MS}"
out_txt="${output_dir}/${output_name}-power.txt"

prog_command="${PYTHON} ${prog_path} --ms ${WAIT_MS}"


echo "[INFO] Running: ${output_name}"
echo "       Command: ${prog_command}"
echo "       Output : ${out_txt}"

sudo "${PYTHON}" "${wrapper_path}" \
    --prog "${prog_command}" \
    --profiler-name ${PROF_NAME} \
    --interval "${INTERVAL}" \
    --output-path "${out_txt}"

echo "[DONE] ${output_name}"
echo

#!/bin/bash

# Script: `profiler.sh`
# Description: Starts `nvidia-smi` in the background until a `Ctrl+C` signal is received.

# Usage: ./profiler <interval> <output_path>
# Example: ./profiler.sh 5 /home/user/logs/output.txt

set -Eeuo pipefail


# --- Colors and styles ---
BOLD="\033[1m"
BLUE="\033[34m"
RED="\033[31m"
YELLOW="\033[33m"
RESET="\033[0m"

# --- Styled tag ---
E3BENCH="${BOLD}${BLUE}e3bench${RESET}"
ERROR_TAG="${RED}ERROR${RESET}"
INFO_TAG="INFO "
WARNING_TAG="${YELLOW}WARN${RESET} "


log_error() {
  echo -e "[$(date '+%Y-%m-%d %H:%M:%S') ${ERROR_TAG}] ${E3BENCH} | $1"
}

log_info() {
  echo -e "[$(date '+%Y-%m-%d %H:%M:%S') ${INFO_TAG}] ${E3BENCH} | $1"
}

log_warn() {
  echo -e "[$(date '+%Y-%m-%d %H:%M:%S') ${WARNING_TAG}] ${E3BENCH} | $1"
}


# --- Argument check ---
if [ "$#" -ne 2 ]; then
  log_error "Invalid tegrastat arguments."
  log_info "Usage: $0 <interval_ms> <output_path>"
  exit 1
fi

INTERVAL_MS=$1
OUTPUT_FILE=$2
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")

# --- Validation ---
if ! [[ "$INTERVAL_MS" =~ ^[0-9]+$ ]]; then
  log_error "Interval must be an integer (milliseconds)."
  exit 1
fi
if [ ! -d "$OUTPUT_DIR" ]; then
  log_error "Directory '$OUTPUT_DIR' does not exist."
  exit 1
fi
if ! command -v nvidia-smi >/dev/null 2>&1; then
  log_error "'nvidia-smi' command not found in PATH."
  exit 1
fi

# Convert ms → fractional seconds for sleep (e.g., 200 → 0.200)
SLEEP_SEC=$(awk -v ms="$INTERVAL_MS" 'BEGIN { printf "%.3f", ms/1000 }')

# Fields to query from nvidia-smi (no units, no header).
# Add/remove fields as needed.
QUERY_FIELDS="imestamp,power.draw.instant,temperature.gpu,utilization.gpu,utilization.memory,name"


# --- Cleanup & traps ---
SAMPLER_PID=""
EXIT_REASON="NORMAL"


cleanup(){
  echo
  if [ -n "$SAMPLER_PID" ] && kill -0 "$SAMPLER_PID" 2>/dev/null; then
    log_info "Stopping nvidia-smi (PID $SAMPLER_PID)..."
    kill "$SAMPLER_PID" 2>/dev/null || true
    sleep 0.2
    kill -9 "$SAMPLER_PID" 2>/dev/null || true
  fi

  case "$EXIT_REASON" in
    CTRLR)  log_warn "Detected Ctrl+R — stopping sampling." ;;
    SIGINT) log_warn "Received Ctrl+C — stopping sampling." ;;
    ERROR)  log_error "An error occurred — stopping sampling." ;;
    CHILD)  log_warn "Sampler exited on its own." ;;
    NORMAL) log_info "Measurement finished normally." ;;
  esac
  log_info "Log file saved at: $OUTPUT_FILE"
}

# --- Trap SIGINT (CTRL+C), EXIT, and ERR signals ---
trap 'EXIT_REASON="SIGINT"; exit 130' SIGINT
trap 'EXIT_REASON="ERROR";  exit 1'   ERR
trap 'cleanup' EXIT


# --- Start sampling ---
log_info "Starting nvidia-smi sampling every ${INTERVAL_MS} ms --> ${OUTPUT_FILE}"

# Create or truncate output file.
: > "$OUTPUT_FILE"

nvidia-smi \
  --query-gpu="${QUERY_FIELDS}" \
  --format=csv \
  --filename="${OUTPUT_FILE}" \
  --loop-ms="${INTERVAL_MS}" &
SAMPLER_PID=$!

log_info "nvidia-smi PID: $SAMPLER_PID"
log_info "Press Ctrl+R to stop."

# Wait for Ctrl+R or child exit
while true; do
  if ! kill -0 "$SAMPLER_PID" 2>/dev/null; then
    EXIT_REASON="CHILD"; break
  fi
  if IFS= read -rsn1 -t 0.2 key; then
    if [[ "$key" == $'\x12' ]]; then  # Ctrl+R
      EXIT_REASON="CTRLR"; break
    fi
  fi
done

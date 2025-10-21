#!/bin/bash

# Script: `profiler.sh`
# Description: Starts `tegrastats` in the background until a `Ctrl + C` signal is received.

# Usage: ./profiler.sh <interval> <output_path>
# Example: ./script.sh 5 /home/user/logs/output.txt

# Ensures any error causes an exit
# `-E`: the ERR trap is inherited in functions/command subshells.
# `-e`: exit immediately if a command fails (non-zero status)
# `-u`: treat undefined variables as errors
# `-o`: fail the whole pipeline if any command fails
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
  log_info "Usage: $0 <interval_in_seconds> <output_path>"
  exit 1
fi

INTERVAL=$1
OUTPUT_FILE=$2
# OUTPUT_FILE="${OUTPUT_DIR%/}/log.txt"
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")

# --- Validation ---
if ! [[ "$INTERVAL" =~ ^[0-9]+$ ]]; then
  log_error "Interval must be an integer (milliseconds)"
  exit 1
fi

# # Create output directory if it doesn't exist
# mkdir -p "$(dirname "$OUTPUT_PATH")"

# Check if output directory exists
if [ ! -d "$OUTPUT_DIR" ]; then
  log_error "Directory '$OUTPUT_DIR' does not exist."
  exit 1
fi


# --- Define cleanup function for SIGINT (CTRL+C), EXIT, and ERR signals ---
cleanup() {
  log_info "Stopping tegrastats..."
  tegrastats --stop >/dev/null 2>&1 || true

  case "$EXIT_REASON" in
    CTRLR)  log_warn "Detected Ctrl+R — stopping tegrastats." ;;
    SIGINT) log_warn "Received Ctrl+C — stopping tegrastats." ;;
    ERROR)  log_error "An error occurred — stopping tegrastats." ;;
    CHILD)  log_warn "tegrastats exited on its own." ;;
    NORMAL) log_info "Measurement finished normally." ;;
  esac
  log_info "Log file saved at: $OUTPUT_FILE"
}

# --- Trap SIGINT (CTRL+C), EXIT, and ERR signals ---
trap 'EXIT_REASON="SIGINT"; exit 130' SIGINT
trap 'EXIT_REASON="ERROR"; exit 1' ERR
trap 'cleanup' EXIT


# --- Main loop ---
log_info "Starting logging every ${INTERVAL}ms to ${OUTPUT_FILE}"

# Create or truncate output file.
: > "$OUTPUT_FILE"

tegrastats --interval "$INTERVAL" --logfile "$OUTPUT_FILE" &
TEGRA_PID=$!

log_info "tegrastats PID: $TEGRA_PID"
log_info "Press Ctrl+R to stop."

# --- Wait for Ctrl+R OR tegrastats exit ---
# Ctrl + R avoid sending SIGINT to child process, and lets main process gracefully handle termination.
while true; do
  if ! kill -0 "$TEGRA_PID" 2>/dev/null; then
    EXIT_REASON="CHILD"
    break
  fi
  if IFS= read -rsn1 -t 0.2 key; then
    if [[ "$key" == $'\x12' ]]; then  # Ctrl+R = 0x12
      EXIT_REASON="CTRLR"
      break
    fi
  fi
done

# tegrastats --interval <int> --logfile <out_file> &

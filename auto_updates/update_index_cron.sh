#!/bin/bash

LOG_FILE="$(dirname "$0")/cron_debug.log"

echo "CRON JOB STARTED: $(date)" >> "$LOG_FILE"

# Update paths as needed
cd "$(dirname "$0")/.." || exit

export HOME=/Users/$(whoami)
export PATH="/Users/aadithya/.pyenv/shims:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

poetry run python mcp_rag_toolkit/update_index_tool.py >> "$LOG_FILE" 2>&1

echo "CRON JOB ENDED: $(date)" >> "$LOG_FILE"
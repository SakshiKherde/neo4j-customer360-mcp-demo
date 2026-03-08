#!/bin/bash
# schedule.sh — add a daily cron job for The Daily Brief
#
# Default: 6:45 AM Pacific (14:45 UTC). Edit CRON_TIME to change.
# Usage: bash scripts/schedule.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON="$PROJECT_DIR/.venv/bin/python"
LOG_DIR="$PROJECT_DIR/logs"
ENV_FILE="$PROJECT_DIR/.env"

mkdir -p "$LOG_DIR"

# 6:45 AM Pacific = 14:45 UTC
CRON_TIME="45 14 * * *"
CRON_CMD="$CRON_TIME cd $PROJECT_DIR && $PYTHON main.py >> $LOG_DIR/daily-brief.log 2>&1"

if crontab -l 2>/dev/null | grep -q "daily-brief\|The Daily Brief"; then
    echo "A cron job for The Daily Brief already exists:"
    crontab -l | grep -E "daily-brief|main\.py"
    echo ""
    read -p "Replace it? [y/N] " confirm
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        crontab -l | grep -v "main\.py" | crontab -
    else
        echo "Aborted."
        exit 0
    fi
fi

(crontab -l 2>/dev/null; echo "# The Daily Brief"; echo "$CRON_CMD") | crontab -

echo "Cron job added:"
echo "  $CRON_CMD"
echo ""
echo "To verify: crontab -l"
echo "Logs will be written to: $LOG_DIR/daily-brief.log"

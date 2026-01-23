#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)
OUTPUT_DIR="$ROOT_DIR/build/profile"
PROFILE_FILE="$OUTPUT_DIR/profile_$(date +%Y%m%d_%H%M%S).prof"

mkdir -p "$OUTPUT_DIR"

echo "Profiling started..."
echo "Output: $PROFILE_FILE"

"$ROOT_DIR/python" -m cProfile -o "$PROFILE_FILE" "$ROOT_DIR/main.py" "$@"

echo ""
echo "Profiling complete: $PROFILE_FILE"
echo ""
echo "View results:"
echo "  snakeviz $PROFILE_FILE"
echo "  $ROOT_DIR/python -m pstats $PROFILE_FILE"

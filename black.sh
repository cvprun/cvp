#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)

USAGE="
Usage: ${BASH_SOURCE[0]} [options]

Available options are:
  -h, --help       Print this message.
  -f, --fix        Edit files in place.
  -i, --in-place   Same '--fix' flag.
  --               Stop handling options.
"

FIX_FLAG=0

function print_error
{
    # shellcheck disable=SC2145
    echo -e "\033[31m$@\033[0m" 1>&2
}

function print_message
{
    # shellcheck disable=SC2145
    echo -e "\033[32m$@\033[0m"
}

function on_interrupt_trap
{
    print_error "An interrupt signal was detected."
    exit 1
}

function print_usage
{
    echo "$USAGE"
}

trap on_interrupt_trap INT

while [[ -n $1 ]]; do
    case $1 in
    -h|--help)
        print_usage
        exit 0
        ;;
    -f|--fix|-i|--in-place)
        FIX_FLAG=1
        shift
        ;;
    --)
        shift
        break
        ;;
    *)
        print_error "Unknown option: $1"
        exit 1
        ;;
    esac
done

ARGS=("--exclude=(/\.git|/\.venv)")
if [[ $FIX_FLAG -eq 0 ]]; then
    ARGS+=("--check" "--diff" "--color")
fi

print_message "black ${ARGS[*]}"

"$ROOT_DIR/python" -m black "${ARGS[@]}" \
    "$ROOT_DIR/cvp/" \
    "$ROOT_DIR/demos/" \
    "$ROOT_DIR/tester/" \
    "$ROOT_DIR/setup.py"

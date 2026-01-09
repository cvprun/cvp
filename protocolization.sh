#!/usr/bin/env bash

ROOT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit; pwd)

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

trap on_interrupt_trap INT

PYTHON="$ROOT_DIR/python"
PROTOS_DIR="${ROOT_DIR}/cvp/protos"
PROTOC_VERSION=$("$PYTHON" -m grpc_tools.protoc --version | sed "s/libprotoc //g")
PYTHON_BIN_DIR=$("$PYTHON" -c "import sysconfig; print(sysconfig.get_path('scripts'))")
PROTOC_GEN_MYPY="${PYTHON_BIN_DIR}/protoc-gen-mypy"
mapfile -t PROTO_FILES < <(find "$PROTOS_DIR" -mindepth 1 -maxdepth 1 -name '*.proto')

if [[ -z "$PROTOC_VERSION" ]]; then
    print_error "The protoc version is unknown"
    print_error "Please install the 'grpcio-tools' package"
    exit 1
fi

if [[ ! -x "$PROTOC_GEN_MYPY" ]]; then
    print_error "Not found protoc-gen-mypy executable"
    print_error "Please install the 'mypy-protobuf' package"
    exit 1
fi

if [[ "${#PROTO_FILES[@]}" -eq 0 ]]; then
    print_error "Not found *.proto files"
    exit 1
fi

ARGS=(
    "--plugin=protoc-gen-mypy=${PYTHON_BIN_DIR}/protoc-gen-mypy"
    "--proto_path=${ROOT_DIR}"
    "--python_out=${ROOT_DIR}"
    "--mypy_out=${ROOT_DIR}"
    "--grpc_python_out=${ROOT_DIR}"
    "${PROTO_FILES[@]}"
)

echo "grpc_tools.protoc version: $PROTOC_VERSION"
echo "protoc-gen-mypy plugin path: $PROTOC_GEN_MYPY"
echo "total proto files: ${#PROTO_FILES[@]}"

print_message "grpc_tools.protoc ${ARGS[*]}"
"$PYTHON" -m grpc_tools.protoc "${ARGS[@]}"

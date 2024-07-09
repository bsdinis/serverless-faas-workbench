#!/usr/bin/env bash

set -xe

function usage() {
    echo "snapshot.sh <junction repo path> <function name>"
    exit 1
}

function kill_junction() {
    sleep $1
    echo "finished sleeping"
    killall junction_run
    echo "killed junction run"
    return 0
}

if [[ $# -lt 1 ]] || [[ $# -gt 2 ]]; then
    usage
fi

JUNCTION_DIR=$1
JUNCTION_BIN="${JUNCTION_DIR}/build/junction/junction_run"
CALADAN_CONFIG="${JUNCTION_DIR}/build/junction/caladan_test.config"
JUNCTION_FAAS_DIR=$(dirname "$(readlink -f "$0")")

if [[ $# -eq 2 ]]; then
    FUNCTION=$2
fi


function snapshot_function() {
    PREFIX="/tmp/functionbench/$1"
    rm -f "${PREFIX}*"

    ${JUNCTION_BIN} ${CALADAN_CONFIG} -S 1 --snapshot-prefix ${PREFIX} -- ${JUNCTION_FAAS_DIR}/venv/bin/python3 ${JUNCTION_FAAS_DIR}/run.py $1
}

function restore_function() {
    PREFIX="/tmp/functionbench/$1"

    ${JUNCTION_BIN} ${CALADAN_CONFIG} -r -- ${PREFIX}.metadata ${PREFIX}.elf
}


function_names=(
"chameleon"             # 0
"float_operation"       # 1
"linpack"               # 2
"matmul"                # 3
"pyaes"                 # 4
"image_processing"      # 5
"rnn_serving"           # 6
"video_processing"      # 7
"lr_training"           # 8
"json_serdes"           # 9: restore broken
"cnn_serving"           # 10: not supported
)

mkdir -p /tmp/functionbench/

if [[ -z "$FUNCTION" ]]; then
    for fname in ${function_names[@]}; do
        echo "$fname"
        snapshot_function $fname
	restore_function $fname
    done
else
    echo "$FUNCTION"
    snapshot_function $FUNCTION
	restore_function $fname
fi

#!/usr/bin/env bash

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

 
if ! command -v nvm >/dev/null 2>&1   ||   ! command -v node >/dev/null 2>&1  ; then
    echo "Node or nvm is not installed"
else
    echo "Node and nvm are installed"
fi




 
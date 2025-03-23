#!/usr/bin/bash

REPO_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 $REPO_PATH/coding-style/main.py $1 $2 $3 $4 $5 $6 $7 $8 $9

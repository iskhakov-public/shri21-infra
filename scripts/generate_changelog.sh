#!/bin/bash

PREV_TAG=$(git describe --abbrev=0 --tags `git rev-list --tags --skip=1 --max-count=1`)
CURRENT_TAG=$(git describe --abbrev=0 --tags `git rev-list --tags --max-count=1`)

echo "CHANGELOG"
echo ----------------------
git log ${PREV_TAG}..${CURRENT_TAG} --pretty=format:'* %h %s'



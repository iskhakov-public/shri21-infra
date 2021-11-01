#!/bin/bash
. ./scripts/env.sh

CURRENT_TAG=$(git describe --abbrev=0 --tags `git rev-list --tags --max-count=1`)
HOTFIXES="${1:-0}"
LASTHASHCOMMIT=$(git rev-list -n 1 ${CURRENT_TAG} | cut -c1-7)
COMMITAUTHOR=$(git rev-list -n 1 ${CURRENT_TAG} --pretty=format:'%an %ae' | awk 'NR==2')

VERSION="${CURRENT_TAG}-${HOTFIXES}-${LASTHASHCOMMIT}"
SUMMARY="test-release: todo-app deploy ${VERSION}"
DESCRIPTION=$(</dev/stdin)
DATE=$(TZ='Europe/Moscow' date "+%F-%H-%M-%S MSK")
ASSIGNEE="iskhakov-nu"
GENERATED="

Date: ${DATE}
By ${COMMITAUTHOR}"

POST="/v2/issues/"
BODY="{\"summary\":\"${SUMMARY}\",\"queue\":\"${QUEUE}\",\"description\":\"${DESCRIPTION} ${GENERATED}\",\"assignee\":\"${ASSIGNEE}\"}"
echo "$BODY"
DATA=$(curl ${GLOBAL_CURL_OPTIONS} -H "${AUTH_HEADER}" -H "${X_ORG_HEADER}" -H "${CONTENT_TYPE_HEADER}" -X POST -d "${BODY}" "${HOST}${POST}")
echo $DATA | jq ".self"
echo $DATA | jq ".key" > res.log 

# curl -H "${AUTH_HEADER}" -H "${X_ORG_HEADER}" -H "${CONTENT_TYPE_HEADER}" -X GET "${HOST}/v2/myself"


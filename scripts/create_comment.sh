#!/bin/bash
. ./scripts/env.sh

# TEXT="Tests completed."
TEXT=$(</dev/stdin)
read ISSUE_ID < res.log

POST="/v2/issues/${ISSUE_ID}/comments"
BODY="{\"text\":\"${TEXT}\"}"

echo "$BODY"
DATA=$(curl ${GLOBAL_CURL_OPTIONS} -H "${AUTH_HEADER}" -H "${X_ORG_HEADER}" -H "${CONTENT_TYPE_HEADER}" -X POST -d "${BODY}" "${HOST}${POST}")
echo $DATA | jq ".self"
# export TASK_KEY = $(echo $DATA | jq ".key" )
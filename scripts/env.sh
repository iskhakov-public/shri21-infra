#!/bin/bash

export OAUTH_YANDEX_TRACKER="${YANDEX_OAUTH}"
export HOST="https://api.tracker.yandex.net"
export AUTH_HEADER="Authorization: OAuth ${OAUTH_YANDEX_TRACKER}"
export X_ORG_HEADER="OrgId:${YANDEX_ORGID}"
export CONTENT_TYPE_HEADER="Content-Type:application/json"
export QUEUE="${YANDEX_QUEUE}"
export GLOBAL_CURL_OPTIONS="--no-progress-meter -s"
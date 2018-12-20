#!/bin/bash
set -eo pipefail

export NEXT=f75877
export PROJECT_NAME="course_catalog"
echo "Next hash is $NEXT"

export WEB_IMAGE=mitodl/${PROJECT_NAME}_web_travis_${NEXT}
export WATCH_IMAGE=mitodl/${PROJECT_NAME}_watch_travis_${NEXT}

echo docker build -t $WEB_IMAGE -f Dockerfile .
echo docker build -t $WATCH_IMAGE -f travis/Dockerfile-travis-watch-build .

echo docker push $WEB_IMAGE
echo docker push $WATCH_IMAGE


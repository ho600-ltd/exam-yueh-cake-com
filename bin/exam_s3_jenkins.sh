#!/bin/bash

WORKSPACE=$1
BUILD_URL=$2
BUILD_NUMBER=$3
REVISION=${4:0:4}
BUILD_TIME=`date +%Y-%m-%dT%H:%M:%S%z`
DIR_NAME=$5

cat << EOF > $WORKSPACE/${DIR_NAME}.yueh-cake.com/__version__.json
{
    "BUILD_URL": "`echo ${BUILD_URL} | sed 's/https\?:\/\/[^\/]\+\//http:\/\/build.dev.null\//'`",
    "BUILD_NUMBER": "${BUILD_NUMBER}",
    "VERSION": "${REVISION}",
    "BUILD_TIME": "${BUILD_TIME}"
}
EOF

sed "s/\${BUILD_NUMBER}/${BUILD_NUMBER}/g" $WORKSPACE/${DIR_NAME}.yueh-cake.com/index.html > $WORKSPACE/${DIR_NAME}.yueh-cake.com/_index.html
sed "s/\${REVISION}/${REVISION}/g" $WORKSPACE/${DIR_NAME}.yueh-cake.com/_index.html > $WORKSPACE/${DIR_NAME}.yueh-cake.com/__index.html
sed "s/\${BUILD_TIME}/${BUILD_TIME}/g" $WORKSPACE/${DIR_NAME}.yueh-cake.com/__index.html > $WORKSPACE/${DIR_NAME}.yueh-cake.com/___index.html
mv $WORKSPACE/${DIR_NAME}.yueh-cake.com/___index.html $WORKSPACE/${DIR_NAME}.yueh-cake.com/index.html
rm -rf $WORKSPACE/${DIR_NAME}.yueh-cake.com/*_index.html

sed "s/\${BUILD_NUMBER}/${BUILD_NUMBER}/g" $WORKSPACE/${DIR_NAME}.yueh-cake.com/jobs.at.ho600/index.html > $WORKSPACE/${DIR_NAME}.yueh-cake.com/jobs.at.ho600/_index.html
sed "s/\${REVISION}/${REVISION}/g" $WORKSPACE/${DIR_NAME}.yueh-cake.com/jobs.at.ho600/_index.html > $WORKSPACE/${DIR_NAME}.yueh-cake.com/jobs.at.ho600/__index.html
sed "s/\${BUILD_TIME}/${BUILD_TIME}/g" $WORKSPACE/${DIR_NAME}.yueh-cake.com/jobs.at.ho600/__index.html > $WORKSPACE/${DIR_NAME}.yueh-cake.com/jobs.at.ho600/___index.html
mv $WORKSPACE/${DIR_NAME}.yueh-cake.com/jobs.at.ho600/___index.html $WORKSPACE/${DIR_NAME}.yueh-cake.com/jobs.at.ho600/index.html
rm -rf $WORKSPACE/${DIR_NAME}.yueh-cake.com/jobs.at.ho600/*_index.html
aws --profile s3-jobs-ho600-com-full-access s3 sync $WORKSPACE/${DIR_NAME}.yueh-cake.com s3://${DIR_NAME}.yueh-cake.com

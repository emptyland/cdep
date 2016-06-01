#!/bin/bash

INCOMING_FILE_NAME='incoming.tmp'
DOWNLOAD_SNAPSHOT_NAME='.download.snapshot'
DOWNLOAD_SNAPSHOT_PATH="third-party/${1}/${DOWNLOAD_SNAPSHOT_NAME}"

# if has downloaded, not again.
if [[ -f ${DOWNLOAD_SNAPSHOT_PATH} ]]; then
    if [[ ${2} == $(cat ${DOWNLOAD_SNAPSHOT_PATH}) ]]; then
        exit 0
    fi
fi

mkdir -p third-party/include
mkdir -p third-party/libs
mkdir -p third-party/${1}

wget ${2} -O "third-party/${1}/${INCOMING_FILE_NAME}"

cd third-party/${1}

typeMsg=$(file ${INCOMING_FILE_NAME})

echo ${typeMsg} | grep 'gzip'
if [[ $? == '0' ]]; then
    tar vxzf "${INCOMING_FILE_NAME}" || exit 1
    echo ${2} > .download.snapshot
fi

echo ${typeMsg} | grep 'Zip'
if [[ $? == '0' ]]; then
    unzip "${INCOMING_FILE_NAME}" || exit 1
    echo ${2} > .download.snapshot
fi

rm ${INCOMING_FILE_NAME}



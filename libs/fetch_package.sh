#!/bin/bash

INCOMING_FILE_NAME='incoming.tmp'

mkdir -p third-party/include
mkdir -p third-party/libs
mkdir -p third-party/${1}

wget --no-check-certificate ${2} -O "third-party/${1}/${INCOMING_FILE_NAME}"

cd third-party/${1}

typeMsg=$(file ${INCOMING_FILE_NAME})

echo ${typeMsg} | grep 'gzip'
if [[ $? == '0' ]]; then
    tar vxzf "${INCOMING_FILE_NAME}" || exit 1
fi

echo ${typeMsg} | grep 'bzip2'
if [[ $? == '0' ]]; then
    tar vxf "${INCOMING_FILE_NAME}" || exit 1
fi

echo ${typeMsg} | grep 'Zip'
if [[ $? == '0' ]]; then
    unzip "${INCOMING_FILE_NAME}" || exit 1
fi

rm ${INCOMING_FILE_NAME}



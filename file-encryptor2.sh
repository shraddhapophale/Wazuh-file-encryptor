#!/bin/bash

file=$3

gpg --pinentry-mode=loopback --passphrase  "root" -o $file.gpg -c $file
mv $file.gpg /opt/encrypted_files

rm $file

ACTION=$1
USER=$2
FILE=$3
PWD=`pwd`

LOCAL=`dirname $0`;
cd $LOCAL
cd ../
filename=$(basename "$0")
LOG_FILE="${PWD}/../logs/active-responses.log"

echo "`date` $0 $1 $2 $3 $4 $5" >> ${LOG_FILE}

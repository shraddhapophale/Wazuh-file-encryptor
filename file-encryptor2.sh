#!/bin/bash

file=$1

gpg --pinentry-mode=loopback --passphrase  "root" -o /opt/cortex+encrypter/Wazuh-file-encryptor/encrypted_files/$file.gpg -c $file

rm $file

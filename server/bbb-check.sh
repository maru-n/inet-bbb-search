#!/usr/bin/env sh
# /usr/local/etc/bbb-check.sh

while read i ; do
    req=`echo ${i} | tr -d '\r' | tr -d '\n'`
    if [ ${req} = "BBB?" ]; then
        echo -n yes
    fi
done

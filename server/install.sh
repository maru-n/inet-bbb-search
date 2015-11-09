#!/usr/bin/env sh

if ! type xinetd 2>/dev/null 1>/dev/null; then
    echo "Please install xinetd."
    return
fi

cp ./bbb-check.sh /usr/local/etc/bbb-check.sh
cp ./bbb-check /etc/xinetd.d/

echo "Restart xinetd by 'sudo service xinetd restart'."

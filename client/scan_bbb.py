#!/usr/bin/env python

from subprocess import Popen, PIPE
import socket


SEARCH_IPS = ["192.168.193.%d"%i for i in range(2,255)]
PORT = 23456

def main():
    ip = scan_bbb(SEARCH_IPS, PORT)
    print(ip)

def scan_bbb(search_ips, port):
    available_ips = []

    pipes = []
    for ip in search_ips:
        pipes.append(Popen(["ping", "-c", "1", "-t", "1", ip], bufsize=1024, stdout=PIPE))

    for p, ip in zip(pipes, search_ips):
        if(p.wait() == 0):
            print('+', end='', flush=True)
            available_ips.append(ip)
        else:
            print('.', end='', flush=True)
    print()

    found_ip = None
    for ip in available_ips:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            s.send(b"BBB?\n")
            if s.recv(8) == b'yes':
                s.close()
                print()
                found_ip = ip
                break
        except Exception as e:
            s.close()
            print('.', end='', flush=True)
    return found_ip


if __name__ == '__main__':
    main()

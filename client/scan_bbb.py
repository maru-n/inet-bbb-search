#!/usr/bin/env python

from subprocess import Popen, PIPE, DEVNULL
import socket


SEARCH_IPS = ["192.168.193.%d"%i for i in range(2,255)]
PORT = 23456

def main():
    ip = scan_bbb(SEARCH_IPS, PORT)
    print(ip)

def scan_bbb(search_ips, port):
    ASYNC_NUM = 256
    available_ips = []

    search_ips_chunk_list = [search_ips[i:min(i+ASYNC_NUM, len(search_ips))] for i in range(0, len(search_ips), ASYNC_NUM)]
    for search_ips_chunk in search_ips_chunk_list:
        pipes = []
        for ip in search_ips_chunk:
            pipes.append(Popen(["ping", "-c", "1", "-t", "1", ip], bufsize=1024, stdout=DEVNULL))

        for p, ip in zip(pipes, search_ips):
            p.wait()
            if(p.returncode == 0):
                print('+', end='', flush=True)
                available_ips.append(ip)
            else:
                print('.', end='', flush=True)
    print()

    found_ip = ""
    for ip in available_ips:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            s.send(b"BBB?\n")
            if s.recv(8) == b'yes':
                s.close()
                found_ip = ip
                break
        except Exception as e:
            s.close()
            print('.', end='', flush=True)
    print()
    return found_ip


if __name__ == '__main__':
    main()

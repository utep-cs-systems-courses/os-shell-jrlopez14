#! /usr/bin/env python3

from os import read, write

def readline(limit = 100):
    curr = 0
    line = ""
    ibuf = read(0,limit)
    sbuf = ibuf.decode()
    while curr < len(sbuf):
        if sbuf[curr] == '\n':
            return line
        line += sbuf[curr]
        curr += 1
        if curr == limit:
            ibuf =  read(0,limit)
            sbuf = ibuf.decode()
            curr = 0
    return ""

def readlines():
    lines = ""
    line = my_readline()
    while line != "":
        lines += line
        line = my_readline()
    return lines

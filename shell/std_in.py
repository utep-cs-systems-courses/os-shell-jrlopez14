#! /usr/bin/env python3

from os import read, write

# Reads the next line entered by user.
def readline(limit = 100):
    curr = 0
    line = ""
    ibuf = read(0,limit)
    sbuf = ibuf.decode()
    while curr < len(sbuf): 
        if sbuf[curr] == '\n': # if character is '\n' return line
            return line
        line += sbuf[curr] # adds each character to line
        curr += 1          # iterates current character
        if curr == limit:  # if end of buffer is reached, read again.
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

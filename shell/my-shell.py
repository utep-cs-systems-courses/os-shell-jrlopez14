#! /usr/bin/env python3

import os, sys, time, re, fileinput
from std_in import readline 
from redirect import input_redirect, output_redirect
from pipes import valid_pipes

pid = os.getpid()

def handle_pipes(args):
    pipe_index = args.index('|')
    left_command = args[0:pipe_index]
    right_command = args[pipe_index+1:]

    pr,pw = os.pipe()
    rc = os.fork()

    if rc < 0:
        sys.exit(1)
    elif rc == 0:
        os.close(1)
        os.dup(pw)
        os.set_inheritable(1,True)
        for fd in (pr,pw):
            os.close(fd)
        if not input_redirect(left_command):
            os.write(2,("Invalid redirect formatting\n").encode())
            sys.exit(1)
        try:
            os.execve(left_command[0], left_command, os.environ)
        except FileNotFoundError:
            pass
        for dir in re.split(":", os.environ['PATH']):
            program = "%s%s" % (dir, left_command[0])
            try:
                os.execve(left_command[0], left_command, os.environ)
            except FileNotFoundError:
                pass
        os.write(2, ("%s: Command not found\n" % left_command[0]).encode())
        sys.exit(1)
    else:
        os.close(0)
        os.dup(pr)
        os.set_inheritable(0,True)
        for fd in(pw,pr):
            os.close(fd)
        if valid_pipes(right_command):
            handle_pipes(right_command)
        if not output_redirect(right_command):
            os.write(2,("Invalid redirect formatting\n").encode())
            sys.exit(1)
        try:
            os.execve(right_command[0], right_command, os.environ)
        except FileNotFoundError:
            pass
        for dir in re.split(":", os.environ['PATH']):
            program = "%s%s" % (dir, right_command[0])
            try:
                os.execve(program, right_command, os.environ)
            except FileNotFoundError:
                pass
        os.write(2, ("%s: command not found\n" % args[0]).encode())
        sys.exit
def main():
    while True:
        if 'PS1' in os.environ:
            os.write(1, ("{}: ".format(os.environ['PS1'])).encode())
        else:
            os.write(1, ("$ ").encode())
    
        input_line = readline().strip()
        if input_line == "":
            continue
        
        args = input_line.split(" ")
        
        if args[0] == "exit":
            os.write(1, ("Process shell finished\n").encode())
            sys.exit(1)
        elif args[0] == "cd":
            if len(args) >= 2:
                try:
                    os.chdir(args[1])
                except:
                    os.write(1,"No such file or directory\n".encode())
                continue
            else:
                os.chdir(os.environ['HOME'])
                continue
        rc = os.fork()
        
        wait = True
        
        if args[-1] == '&':
            wait = False
            args.pop()
        if rc < 0:
            sys.exit(1)
        elif rc == 0:                   # child
            if valid_pipes(args):
                handle_pipes(args)
            if not (input_redirect(args) and output_redirect(args)):
                os.write(2, ("Invalid redirect formatting\n").encode())
                continue
            try:
                os.execve(args[0], args, os.environ)
            except FileNotFoundError:
                pass
            for dir in re.split(":", os.environ['PATH']): # try each directory in the path
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program, args, os.environ) # try to exec program
                except FileNotFoundError:             # ...expected
                    pass                              # ...fail quietly
            os.write(2, ("%s: Command not found\n" % args[0]).encode())
            sys.exit(1)       
        else:                           # parent (forked ok)
            if wait:
                childPidCode = os.wait()

if __name__ == "__main__":
    main()

#! /usr/bin/env python3

import os, sys, time, re, fileinput
from std_in import readline 
from redirect import input_redirect, output_redirect
from pipes import valid_pipes

pid = os.getpid()

# trys to execute the command from each directory in the path
def exec_cmd(args):
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
        

# Piping allows the output of one command to be the input of another
def handle_pipes(args):
    pipe_index = args.index('|')
    left_command = args[0:pipe_index]
    right_command = args[pipe_index+1:]

    pr,pw = os.pipe()
    rc = os.fork()

    if rc < 0:     # fork failed
        sys.exit(1)
    elif rc == 0:  # if child
        os.close(1)
        os.dup(pw)
        os.set_inheritable(1,True)
        for fd in (pw,pr):
            os.close(fd)
        if not input_redirect(left_command):  # handles input redirection
            os.write(2,("Invalid redirect formatting\n").encode())
            sys.exit(1)
        exec_cmd(left_command) # executes command
    else:
        os.close(0)
        os.dup(pr)
        os.set_inheritable(0,True)
        for fd in(pw,pr):
            os.close(fd)
        if valid_pipes(right_command): # handles remaining pipes, if any
            handle_pipes(right_command)
        elif not output_redirect(right_command): # handles output redirections, if any
            os.write(2,("Invalid redirect formatting\n").encode())
            sys.exit(1)
        exec_cmd(right_command) # executes command

def main():
    while True:
        if 'PS1' in os.environ:
            os.write(2, ("{}: ".format(os.environ['PS1'])).encode())
        else:
            os.write(2, ("$ ").encode())
    
        input_line = readline().strip()

        # if no input is given, continue. (returns to beginning of loop)
        if input_line == "":
            continue
        
        args = input_line.split(" ")

        # if exit is entered, the shell will terminate
        if args[0].lower() == "exit":
            os.write(2, ("Process shell finished\n").encode())
            sys.exit(1)
        elif args[0] == "cd":
            if len(args) >= 2:
                try:
                    os.chdir(args[1])
                except:
                    os.write(2,"No such file or directory\n".encode())
            else:
                os.chdir(os.environ['HOME'])
            continue

        # creates two processes. a parent process and a child process.
        rc = os.fork()

        # Parent should wait.
        wait = True
        if args[-1] == '&': # Parent shouldn't wait
            wait = False 
            args.pop()

            
        if rc < 0: # if fork failed
            sys.exit(1)
        elif rc == 0:                   # if child process
            if valid_pipes(args):    # if there is a pipe and the left and right commands are well
                handle_pipes(args)   # formatted.
            elif not (input_redirect(args) and output_redirect(args)): # if redirects, handle those
                os.write(2, ("Invalid redirect formatting\n").encode()) # and verify well formatted
                continue
            exec_cmd(args)
        else:                           # parent (forked ok)
            if wait:
                childPidCode = os.wait()

if __name__ == "__main__":
    main()

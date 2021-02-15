#! /usr/bin/env python3

import os, sys, time, re
import my_std_in

pid = os.getpid()

#os.write(1, ("About to fork (pid:%d)\n" % pid).encode())

while True:
    args = my_std_in.readline().split(" ")
    if args[0] == "exit":
        os.write(1, ("Process shell finished\n").encode())
        sys.exit(1)
    rc = os.fork()
    if rc < 0:
        #os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())
        
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            #os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
            try:
                 os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                 pass                              # ...fail quietly
        os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
        sys.exit(1)       

    else:                           # parent (forked ok)
        #os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % (pid, rc)).encode())
        childPidCode = os.wait()
        #os.write(1, ("Parent: Child %d terminated with exit code %d\n" % childPidCode).encode())

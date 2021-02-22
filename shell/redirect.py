#! /usr/bin/env python3

import os

# Redirects command output to specified location
# If True, redirections were handled properly, if any.
def output_redirect(args):
    if '>' in args:
        goes_into_index = args.index('>')
        # Removes the redirection part of command.
        args.pop(goes_into_index)
        output_file = args.pop(goes_into_index)
        # Cannot have multiple output redirections in command.
        if '>' not in args:
            os.close(1)
            os.open(output_file, os.O_CREAT | os.O_WRONLY)
            os.set_inheritable(1,True)
            return True
        else:
            return False
    return True

# Redirects command input to specified location.
# If True, redirections were handled properly, if any.
def input_redirect(args):
    if '<' in args:
        from_index = args.index('<')
        # Removes the redirection part of command.
        args.pop(from_index)
        input_file = args.pop(from_index)
        # Cannot have multiple input redirections in command.
        if '<' not in args:
            os.close(0)
            os.open(input_file, os.O_RDONLY)
            os.set_inheritable(0,True)
            return True
        else:
            return False
    return True
 

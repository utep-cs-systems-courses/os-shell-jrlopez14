#! /usr/bin/env python3

import os

def output_redirect(args):
    if '>' in args:
        goes_into_index = args.index('>')
        args.pop(goes_into_index)
        output_file = args.pop(goes_into_index)
        if '>' not in args:
            os.close(1)
            os.open(output_file, os.O_CREAT | os.O_WRONLY)
            os.set_inheritable(1,True)
            return True
        else:
            return False
    return True
def input_redirect(args):
    if '<' in args:
        from_index = args.index('<')
        args.pop(from_index)
        input_file = args.pop(from_index)
        if '<' not in args:
            os.close(0)
            os.open(input_file, os.O_RDONLY)
            os.set_inheritable(0,True)
            return True
        else:
            return False
    return True

#! /usr/bin/env python3

def valid_pipes(args):
    pipe_index = -1
    if '|' in args:
        pipe_index = args.index('|')
    else:
        return False
    
    left_command = args[:pipe_index]
    right_command = args[pipe_index+1:]
    
    if '>' in left_command or '<' in right_command:
        return False
    elif left_command.count('<') > 1 or right_command.count('>') > 1:
        return False
    return True

#! /usr/bin/env python3

# Checks if pipes exist. If Pipes exist and they are well formatted, return True.
# Otherwise false.

def valid_pipes(args):
    pipe_index = -1
    if '|' in args:
        pipe_index = args.index('|')
    else:
        return False
    
    left_command = args[:pipe_index]
    right_command = args[pipe_index+1:]

    # Cannot redirect output on left command and can't redirect input for right command.
    if '>' in left_command or '<' in right_command:
        return False
    # Checks if one redirection for each command. 
    elif left_command.count('<') > 1 or right_command.count('>') > 1:
        return False
    return True

#!/usr/bin/env python

from os import getcwd
import sys

def main(wanted):

    # This only works with directory names, not paths
    if "/" in wanted:
        return wanted

    # See where we are
    path = getcwd().split("/")
    if wanted[0] == '+':
        try:
            n = int(wanted[1:])
        except ValueError:
            sys.stderr.write("Error: + must be followed by a number.")
            return "."
        return "/".join(path[:-n])
    else:
        for i in range(len(path)-1, -1, -1):
            if path[i] == wanted:
                return "/".join(path[:i+1])
    return wanted

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.stdout.write(main(sys.argv[1]) + "\n")

        
        
    

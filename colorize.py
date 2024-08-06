#!/usr/bin/env python

import sys

from BIutils import BItext

def usage():
    sys.stdout.write("""colorize.py - Add colors to strings

Usage: colorize.py [-h] [text color]...

This command acts as a filter, reading text lines from stdin and writing
them out to stdout. If an occurrence of `text' is found in the input, it
is written out in the specified `color'. Valid colors are:

  {}

A color name can be preceded by `+' to to highlight it. Multiple pairs of
text and color can be supplied. 

NOTE: an entry cannot partially overlap one that appears before it on the 
command line. For example, given:

  colorize.py APPLES red LEMON yellow

if the input contains `APPLEMON', the LEMON string will not be colored.

""".format(" ".join(BItext._colors)))

if __name__ == "__main__":
    args = sys.argv[1:]
    if args == [] or "-h" in args or "--help" in args:
        usage()
        sys.exit(0)

    matchers = []
    for i in range(0, len(args), 2):
        color = args[i+1]
        if BItext.isColor(color):
            matchers.append(BItext.Matcher(args[i], args[i+1]))
        else:
            sys.stderr.write("Warning: unknown color `{}'.\n".format(color))

    if matchers:
        M = BItext.MultiMatcher(matchers)
        for line in sys.stdin:
            for ch in line:
                M.match(ch)
    else:
        sys.exit(1)




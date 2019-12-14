#!/usr/bin/env python

import sys

class Enumerator(object):
    v = 1
    step = 1
    inputs = []
    argsmode = False

    def parseArgs(self, args):
        prev = ""
        if "-h" in args or "--help" in args:
            self.usage()
            return False
        for a in args:
            if prev == "-i":
                self.v = int(a)
                prev = ""
            elif prev == "-s":
                self.step = int(a)
                prev = ""
            elif a in ["-i", "-s"]:
                prev = a
            elif a == "-a":
                self.argsmode = True
            else:
                self.inputs.append(a)
        if not self.argsmode and not self.inputs:
            self.inputs = ["/dev/stdin"]
        return True

    def usage(self):
        sys.stdout.write("""enumerate.py - add numbers to lines of files

Usage: enumerate.py [options] inputs...

This program prints the contents of the files named as inputs, prepending each
line with a progressive number followed by a tab. If multiple files are specified,
they are read consecutively and numbering progresses across all of them. If no 
inputs are specified, reads standard input. If -a is supplied, the command line 
arguments are enumerated (instead of being treated as filenames).

Options:
  -i I | Start numbering at I (default: 1)
  -s S | Increase line number by S (default: 1)
  -a   | Enumerate command-line arguments.

""")

    def run(self):
        if self.argsmode:
            for i in self.inputs:
                sys.stdout.write("{}\t{}\n".format(self.v, i))
                self.v += self.step
        else:
            for infile in self.inputs:
                with open(infile, "r") as f:
                    for line in f:
                        sys.stdout.write("{}\t{}".format(self.v, line))
                        self.v += self.step

if __name__ == "__main__":
    args = sys.argv[1:]
    E = Enumerator()
    if E.parseArgs(args):
        E.run()

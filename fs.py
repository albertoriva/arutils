#!/usr/bin/env python

import os
import sys
import glob

def sizeof_fmt(num):
    for unit in [' B','KB','MB','GB','TB','PB','EB','ZB']:
        if abs(num) < 1024.0:
            return "%3.1f %s" % (num, unit)
        num /= 1024.0
    return "%.1f %s" % (num, 'YB')

class FS():
    files = []
    human = False
    csv = False
    recurse = False
    totonly = False
    
    def __init__(self):
        self.files = []

    def usage(self):
        sys.stdout.write("""fs.py - Display total size of a set of files.

Usage: fs.py [options] [filespecs...]

Each filespec can be: the name of an existing file or directory, or a specifier
of the form @filename, in which case the list of filespecs is read from file
`filename'. If no filespecs are supplied, uses all files in the current directory.

Options:

  -u | Output sizes in the appropriate unit of measure (e.g. MB, GB) instead of
       number of bytes.
  -c | Print output as tab-delimited: sizes in first column, filenames in second.
  -r | Recurse into subdirectories.
  -t | Only print final total to standard output.
  -s | Read list of filespecs from standard input.

""")

    def parseArgs(self, args):
        fromStdin = False

        if "-h" in args or "--help" in args:
            self.usage()
            return False
        for a in args:
            if a == "-u":
                self.human = True
            elif a == "-c":
                self.csv = True
            elif a == "-r":
                self.recurse = True
            elif a == "-t":
                self.totonly = True
            elif a == "-s":
                fromStdin = True
                self.fromStdin()
            else:
                self.files.append(a)

        if len(self.files) == 0 and not fromStdin:
            self.files = glob.glob("*")
        return True

    def fromStdin(self):
        while True:
            f = sys.stdin.readline()
            if f:
                self.files.append(f.rstrip("\r\n"))
            else:
                return

    def write_size(self, f, prefix):
        try:
            info = os.stat(f)
            size = info.st_size

            if self.human:
                psize = sizeof_fmt(size)
            else:
                psize = size

            if self.csv:
                print "{0}\t{1}".format(psize, prefix + os.path.basename(f))
            elif self.totonly:
                pass
            else:
                print "{0:>12} {1}".format(psize, prefix + os.path.basename(f))
            return size
        except:
            if self.csv:
                print "???\t{0}".format(prefix + os.path.basename(f))
            elif self.totonly:
                pass
            else:
                print "{0:>12} {1}".format("???", prefix + os.path.basename(f))
            return 0

    def run(self, files, prefix, top=False):
        total = 0

        for f in files:
            if f[0] == "@":       # starts with @?
                fl = f[1:]
                if os.path.exists(fl):
                    with open(fl, "r") as flin:
                        for fname in flin:
                            total += self.write_size(fname.rstrip("\r\n"), prefix)
            elif not os.path.exists(f): # File does not exist?
                psize = "???"
            elif not os.path.isfile(f): # Is it a directory?
                if top or self.recurse:
                    subfiles = glob.glob(f + "/*")
                    total += self.run(subfiles, prefix + f + "/")
            else:
                total += self.write_size(f, prefix)

        if top:
            # print "Top={}, prefix={}, files={}, total={}".format(top, prefix, len(files), total)
            if self.human:
                ptotal = sizeof_fmt(total)
            else:
                ptotal = total
            if self.csv:
                sys.stdout.write("{}\t*** Total ***\n".format(ptotal))
            elif self.totonly:
                sys.stdout.write("{}\n".format(ptotal))
            else:
                sys.stdout.write("\n{0:>12} *** Total ***\n".format(ptotal))
        return total

# def do_fs(files, human=False, csv=False, recurse=False, prefix='', totonly=False):
#     if csv:
#         mode = "csv"
#     elif totonly:
#         mode = "tot"
#     else:
#         mode = "norm"
#     total = 0
#     for f in files:

#         if f[0] == "@":       # starts with @?
#             fl = f[1:]
#             if os.path.exists(fl):
#                 with open(fl, "r") as flin:
#                     for fname in flin:
#                         total += write_size(fname.rstrip("\r\n"), prefix, mode)
#         elif not os.path.exists(f): # File does not exist?
#             psize = "???"
#         elif not os.path.isfile(f): # Is it a directory?
#             if recurse:
#                 subfiles = glob.glob(f + "/*")
#                 # print "Recursing, {}".format(subfiles)
#                 total += do_fs(subfiles, human=human, csv=csv, recurse=recurse, prefix=prefix+f+"/")
#         else:
#             total += write_size(f, csv, prefix)

#     if human:
#         ptotal = sizeof_fmt(total)
#     else:
#         ptotal = total
#     if prefix == '':
#         if csv:
#             print "{}\t*** Total ***".format(ptotal)
#         else:
#             print
#             print "{0:>12} *** Total ***".format(ptotal)
#     return total

if __name__ == "__main__":
    fs = FS()
    if fs.parseArgs(sys.argv[1:]):
        fs.run(fs.files, '', top=True)
    #do_fs(files, human=human, csv=csv, recurse=recurse, totonly=totonly)

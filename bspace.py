#!/usr/bin/env python

import os
import sys
import subprocess

# bs download run --name millerlab1 -o test

COMMANDS = ["list", "meta", "info", "initdir", "all"]

class BSClient():
    command = None
    args = []

    def parseArgs(self, args):
        if not args:
            self.usage()
            return False
        if args[0] in COMMANDS:
            self.command = args[0]
        else:
            sys.stderr.write("Unknown command: {}.\n".format(args[0]))
            return False
        self.args = args[1:]
        return True

    def usage(self):
        sys.stdout.write("""bspace.py - Wrapper for BaseSpace command-line interface.

Usage: bspace.py command arguments...

Where command is one of: {}

""".format(",".join(COMMANDS)))

    def callBS(self, arguments, csv=True):
        """Low-level method to call bs with the supplied arguments, adding the flag for csv output
(unless `csv' is False). Returns  command output as a string."""
        cmdline = "bs " + " ".join(arguments)
        if csv:
            cmdline += " -f csv"
        return subprocess.check_output(cmdline, shell=True)

    def getRunInfo(self, name):
        """Get all information on run `name'. Returns a list of pairs (key, value) in the order in which they were retrieved from BaseSpace."""
        p = self.callBS(["run", "get", "--name", name])
        lines = p.split("\n")
        hdr = lines[0].strip().split(",")
        data = lines[1].strip().split(",")
        return zip(hdr, data)

    def writeRunInfo(self, filename, runinfo):
        """Write run data `runinfo' to `filename' in tab-delimited format."""
        with open(filename, "w") as out:
            for pair in runinfo:
                out.write("{}\t{}\n".format(*pair))

    def writeEntry(self, stream, d, label, key):
        stream.write("{}:\t{}\n".format(label, d[key]))

    def writeMeta(self, filename, runinfo):
        d = dict(runinfo)
        with open(filename, "w") as out:
            self.writeEntry(out, d, "Name", "ExperimentName")
            self.writeEntry(out, d, "ID", "Id")
            self.writeEntry(out, d, "URL", "BaseSpaceUIHref.HrefBaseSpaceUI")
            self.writeEntry(out, d, "BasespaceName", "Name")
            self.writeEntry(out, d, "Instrument", "InstrumentName")
            self.writeEntry(out, d, "Flowcell", "FlowcellBarcode")
            self.writeEntry(out, d, "Date", "DateCreated")
            out.write("Description:\t\n")

    def initializeDirectory(self, name):
        os.mkdir(name)
        ri = self.getRunInfo(name)
        self.writeRunInfo(name + "/runInfo.csv", ri)
        self.writeMeta(name + "/META", ri)
        os.mkdir(name + "/fastq")

    def getAllRuns(self, show=False):
        if show:
            p = self.callBS(["run", "list"], csv=False)
            sys.stdout.write(p)
            return
        result = []
        p = self.callBS(["run", "list"])
        rows = [ line.strip() for line in p.split("\n") ]
        hdr = rows[0].split(",")
        for line in rows[1:]:
            fields = line.strip().split(",")
            result.append(dict(zip(hdr, fields)))
        return result

    def initializeAllDirectories(self):
        runs = self.getAllRuns()
        for run in runs:
            name = run["ExperimentName"]
            sys.stderr.write("{}... ".format(name))
            self.initializeDirectory(name)
            sys.stderr.write("done.\n")

    def main(self):
        if self.command == "list":
            self.getAllRuns(show=True)
        elif self.command == "initdir":
            for name in self.args:
                self.initializeDirectory(name)
        elif self.command == "all":
            self.initializeAllDirectories()

if __name__ == "__main__":
    B = BSClient()
    if B.parseArgs(sys.argv[1:]):
        B.main()

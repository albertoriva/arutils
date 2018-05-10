#!/usr/bin/env python

import sys
import time
import curses
from curses.wrapper import wrapper

class TDFile():
    filename = None
    label = ""
    delim = None
    data = []
    nrows = 0
    ncols = 0
    colsizes = None
    row = 0
    col = 0
    gap = 1
    maxrows = 1000
    header = False
    
    def __init__(self, filename):
        self.filename = filename
        if not self.delim:
            self.delim = self.detectDelimiter()
        rows_read = 0
        with open(self.filename, "r") as f:
            for line in f:
                parsed = line.rstrip("\r\n").split(self.delim)
                self.nrows += 1
                if self.colsizes:
                    for i in range(self.ncols):
                        self.colsizes[i] = max(self.colsizes[i], len(parsed[i]))
                else:
                    self.ncols = len(parsed)
                    self.colsizes = [len(w) for w in parsed]
                self.data.append(parsed)
                rows_read += 1
                if rows_read >= self.maxrows:
                    break
        # print (self.nrows, self.ncols, self.colsizes)

    def detectDelimiter(self):
        hits = {'\t': 0, ',': 0, ';': 0, ':': 0}
        with open(self.filename, "r") as f:
            for i in range(5):
                line = f.readline()
                for ch in line:
                    if ch in hits:
                        hits[ch] += 1
        best = ''
        bestc = 0
        for (ch, count) in hits.iteritems():
            if count > bestc:
                best = ch
        return best

    def writeLine(self, win, ypos, w, rdata, attr):
        xpos = 0
        c = self.col
        while True:
            if xpos + self.colsizes[c] >= w:
                break
            win.addstr(rdata[c], attr)
            xpos += self.colsizes[c] + self.gap
            if xpos >= w:
                break
            win.move(ypos, xpos)
            c += 1
            if c >= self.ncols:
                break

    def display(self, win):
        """Display the current view of the file in window `win'."""
        (h, w) = win.getmaxyx()
        ypos = 0
        r = self.row
        win.move(0, 0)
        win.erase()
        if self.header:
            self.writeLine(win, 0, w, self.data[0], curses.A_BOLD)
            ypos = 1
            win.move(1, 0)
            if r == 0:
                r = 1
        maxrow = h - 1
        while True:
            rdata = self.data[r]
            self.writeLine(win, ypos, w, rdata, curses.A_NORMAL)
            r += 1
            ypos += 1
            xpos = 0
            if ypos == maxrow or r == self.nrows:
                break
            win.move(ypos, xpos)
        win.move(maxrow, 0)
        win.addstr("{} | Row: {} Col: {}".format(self.label, self.row + 1, self.col + 1), curses.A_BOLD)
        win.refresh()

    def left(self):
        if self.col > 0:
            self.col += -1

    def right(self):
        self.col += 1
        if self.col == self.ncols:
            self.col += -1

    def up(self):
        if self.row > 0:
            self.row += -1

    def down(self):
        self.row += 1
        if self.row == self.nrows:
            self.row += -1

    def top(self):
        self.row = 0

    def bottom(self):
        self.row = self.nrows - 1

    def askRow(self, win):
        (h, w) = win.getmaxyx()
        win.move(h-1, 0)
        win.clrtoeol()
        win.addstr("Enter row number: ", curses.A_BOLD)
        try:
            curses.echo()
            r = win.getstr()
        finally:
            curses.noecho()
        try:
            r = int(r)
            if r <= 0 or r > self.nrows:
                return
            self.row = r - 1
        except ValueError:
            pass

    def askColumn(self, win):
        (h, w) = win.getmaxyx()
        win.move(h-1, 0)
        win.clrtoeol()
        win.addstr("Enter column number: ", curses.A_BOLD)
        try:
            curses.echo()
            c = win.getstr()
        finally:
            curses.noecho()
        try:
            c = int(c)
            if c <= 0 or c > self.ncols:
                return
            self.col = c - 1
        except ValueError:
            pass

def run(win):
    curses.curs_set(0)
    while True:
        FILE.display(win)
        a = win.getch()
        if a in [113, 81]:      # Quit (q, Q)
            break
        elif a == curses.KEY_RIGHT:
            FILE.right()
        elif a == curses.KEY_LEFT:
            FILE.left()
        elif a == curses.KEY_UP:
            FILE.up()
        elif a == curses.KEY_DOWN:
            FILE.down()
        elif a == curses.KEY_HOME:
            FILE.top()
        elif a == curses.KEY_END:
            FILE.bottom()
        elif a == ord('r'):
            FILE.askRow(win)
        elif a == ord('c'):
            FILE.askColumn(win)
        elif a == ord('+'):
            FILE.gap += 1
        elif a == ord('-'):
            if FILE.gap > 0:
                FILE.gap -= 1
        elif a == ord('h'):
            FILE.header = not FILE.header
        elif a == 350:       # Keypad 5
            FILE.col = 0
            FILE.top()

def decodeDelimiter(a):
    if a == 'tab':
        return '\t'
    else:
        return a
    
def parseArgs(args):
    if "-h" in args:
        return []
    prev = ""
    filenames = []
    for a in args:
        if prev == "-m":
            TDFile.maxrows = int(a)
            prev = ""
        elif prev == "-d":
            TDfile.delimiter = decodeDelimiter(a)
            prev = ""
        elif a in ["-m", "-d"]:
            prev = a
        elif a == '-b':
            TDFile.header = True
        else:
            filenames.append(a)
    return filenames

def usage():
    sys.stdout.write("""tv.py - viewer for delimited files

Usage: tv.py [options] filenames...

Options:
  -d D | Use character D as delimiter (use 'tab' for tab). Default: autodetect.
  -m M | Read the first M lines from each input file (default: {}).
  -b   | Enable header mode (first line bold and always visible).

While displaying a file, the following keys can be used:

  arrow keys | move up, down, left, right
  Home, End  | go to top or bottom of file respectively
  keypad '5' | go to first line, first column
  r          | prompt for row number, jump to it
  c          | prompt for column number, jump to it
  h          | toggle header mode
  +/-        | increase, decrease gap between columns
  q, Q       | quit

""")

if __name__ == "__main__":
    global FILE
    filenames = parseArgs(sys.argv[1:])
    nf = 1
    totf = len(filenames)
    if filenames:
        for filename in filenames:
            FILE = TDFile(filename)
            if totf == 1:
                FILE.label = filename
            else:
                FILE.label = "{} ({}/{})".format(filename, nf, totf)
            wrapper(run)
            nf += 1
    else:
       usage()     

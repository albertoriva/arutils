#!/usr/bin/env python

import sys
import time
import curses
from curses.wrapper import wrapper

class TDFile():
    filename = None
    data = []
    nrows = 0
    ncols = 0
    colsizes = None
    row = 0
    col = 0
    gap = 1
    
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, "r") as f:
            for line in f:
                parsed = line.rstrip("\r\n").split("\t")
                self.nrows += 1
                if self.colsizes:
                    for i in range(self.ncols):
                        self.colsizes[i] = max(self.colsizes[i], len(parsed[i]))
                else:
                    self.ncols = len(parsed)
                    self.colsizes = [len(w) for w in parsed]
                self.data.append(parsed)
        # print (self.nrows, self.ncols, self.colsizes)

    def display(self, win):
        """Display the current view of the file in window `win'."""
        (h, w) = win.getmaxyx()
        ypos = 0
        r = self.row
        win.move(0, 0)
        win.erase()
        while True:
            rdata = self.data[r]
            xpos = 0
            c = self.col
            while True:
                if xpos + self.colsizes[c] >= w:
                    break
                if r == 0:
                    win.addstr(rdata[c], curses.A_BOLD)
                else:
                    win.addstr(rdata[c])
                xpos += self.colsizes[c] + self.gap
                if xpos >= w:
                    break
                win.move(ypos, xpos)
                c += 1
                if c >= self.ncols:
                    break
            r += 1
            ypos += 1
            xpos = 0
            if r == h or r == self.nrows:
                break
            win.move(ypos, xpos)
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
            
def run(win):
    while True:
        FILE.display(win)
        a = win.getch()
        if a in [113, 81]:
            break
        elif a == curses.KEY_RIGHT:
            FILE.right()
        elif a == curses.KEY_LEFT:
            FILE.left()
        elif a == curses.KEY_UP:
            FILE.up()
        elif a == curses.KEY_DOWN:
            FILE.down()
        elif a == ord('+'):
            FILE.gap += 1
        elif a == ord('-'):
            FILE.gap -= 1

if __name__ == "__main__":
    global FILE
    FILE = TDFile(sys.argv[1])
    wrapper(run)
    

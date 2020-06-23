#!/usr/bin/env python

import sys
from BIutils import BIbs

if __name__ == "__main__":
    B = BIbs.BSClient()
    if B.parseArgs(sys.argv[1:]):
        B.main()

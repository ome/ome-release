#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fileinput

from utils import RSYNC_PATH
from doc_generator import find_pkg, repl_all


def usage():
    print "mtoolsgen.py version"
    sys.exit(1)


try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y"),
        "@YEAR@": datetime.datetime.now().strftime("%Y")}

PREFIX = os.environ.get('PREFIX', 'mtools')
MTOOLS_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

for x, y in (
        ("MTOOLS_WIN", "OMERO.mtools_@VERSION@_win.zip"),
        ("MTOOLS_MAC", "OMERO.mtools_@VERSION@_mac.zip"),
        ("MTOOLS_WIN_MCR", "OMERO.mtools_@VERSION@_win_mcr.zip"),
        ("MTOOLS_MAC_MCR", "OMERO.mtools_@VERSION@_mac_mcr.zip"),
        ):

    find_pkg(repl, MTOOLS_RSYNC_PATH, x, y)

for line in fileinput.input(["mtools_downloads.html"]):
    print repl_all(repl, line, check_http=True),

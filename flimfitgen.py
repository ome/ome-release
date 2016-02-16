#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import datetime
import fileinput

from doc_generator import find_pkg, repl_all


def usage():
    print "flimfitgen.py version"
    sys.exit(1)

try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

RSYNC_PATH = os.environ.get('RSYNC_PATH', '/ome/data_repo/public/')
PREFIX = os.environ.get('PREFIX', 'flimfit')
FLIMFIT_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

# Links to the MCR downloads
repl["@MCR_WIN@"] = "http://www.mathworks.com/supportfiles/downloads/R2014b" \
    "/deployment_files/R2014b/installers/win64/MCR_R2014b_win64_installer.exe"
repl["@MCR_MAC@"] = "http://www.mathworks.com/supportfiles/downloads/R2014b" \
    "/deployment_files/R2014b/installers/maci64" \
    "/MCR_R2014b_maci64_installer.zip"

for x, y in (
        ("FLIMFIT_51_WIN", "artifacts/FLIMfit_@VERSION@_x64.zip"),
        ("FLIMFIT_51_MAC", "artifacts/FLIMfit_@VERSION@_MACI64.zip"),
        ):

    find_pkg(repl, FLIMFIT_RSYNC_PATH, x, y)


for line in fileinput.input(["flimfit_downloads.html"]):
    print repl_all(repl, line, check_http=True),

#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import glob
import hashlib
import httplib
import datetime
import urlparse
import fileinput


# For calculating tags
import github

from doc_generator import *


fingerprint_url = "http://hudson.openmicroscopy.org.uk/fingerprint"
MD5s = []


def usage():
    print "gen.py version build [build_ice34]"
    sys.exit(1)

try:
    version = sys.argv[1]
    build = sys.argv[2]
except:
    usage()

repl = {"@VERSION@": version,
        "@BUILD@": build,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

# Read major version from input version
import re
split_version =  re.split("^([0-9]+)\.([0-9]+)\.([0-9]+)(.*?)$", version)
major_version = int(split_version[1])

gh = github.Github(user_agent="PyGithub")
ome = "openmicroscopy"
scc = "snoopycrimecop"

repo1 = gh.get_organization(ome).get_repo(ome)
repo2 = gh.get_user(scc).get_repo(ome)

for repo in (repo1, repo2):
    for tag in repo.get_tags():
        if tag.name == ("v.%s" % version):
            break
        tag = None  # Disallow fall-through

repl["@SHA1_FULL@"] = tag.commit.sha
repl["@SHA1_SHORT@"] = tag.commit.sha[0:10]
repl["@DOC_URL@"] = "https://www.openmicroscopy.org/site/support/omero%s" % major_version
if "STAGING" in os.environ and os.environ.get("STAGING"):
    repl["@DOC_URL@"] += "-staging"

if "SNAPSHOT_PATH" in os.environ:
    SNAPSHOT_PATH =  os.environ.get('SNAPSHOT_PATH')
else:
    SNAPSHOT_PATH = "/ome/data_repo/public/"

OMERO_SNAPSHOT_PATH = SNAPSHOT_PATH + "/omero/"

if "ANNOUCEMENT_URL" in os.environ:
    repl["@ANNOUCEMENT_URL@"] = os.environ.get('ANNOUCEMENT_URL')
else:
    repl["@ANNOUCEMENT_URL@"] = "https://www.openmicroscopy.org/community/viewforum.php?f=11"

if "MILESTONE" in os.environ:
    repl["@MILESTONE@"] = os.environ.get('MILESTONE')
else:
    repl["@MILESTONE@"] = "OMERO-%s" % version

for x, y in (
    ("LINUX_CLIENTS", "@VERSION@/OMERO.clients-@VERSION@-ice33-@BUILD@.linux.zip"),
    ("MAC_CLIENTS", "@VERSION@/OMERO.clients-@VERSION@-ice33-@BUILD@.mac.zip"),
    ("WIN_CLIENTS", "@VERSION@/OMERO.clients-@VERSION@-ice33-@BUILD@.win.zip"),
    ("IJ_CLIENTS", "@VERSION@/OMERO.insight-ij-@VERSION@-ice33-@BUILD@.zip"),
    ("MATLAB_CLIENTS", "@VERSION@/OMERO.matlab-@VERSION@-ice33-@BUILD@.zip"),
    ("SERVER33", "@VERSION@/OMERO.server-@VERSION@-ice33-@BUILD@.zip"),
    ("SERVER34", "@VERSION@/OMERO.server-@VERSION@-ice34-@BUILD@.zip"),
    ("SERVER35", "@VERSION@/OMERO.server-@VERSION@-ice35-@BUILD@.zip"),
    ("DOCS", "@VERSION@/OMERO.docs-@VERSION@-ice33-@BUILD@.zip"),
    ("VM", "@VERSION@/omero-@VERSION@-@BUILD@.ova"),
    ("DOC", "@VERSION@/OMERO-@VERSION@.pdf")
    ):

    find_pkg(repl, fingerprint_url, OMERO_SNAPSHOT_PATH, x, y, MD5s)


for line in fileinput.input(["tmpl.txt"]):
    print repl_all(repl, line, check_http=True),

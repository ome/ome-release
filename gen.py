#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import datetime
import fileinput

from doc_generator import find_pkg, repl_all

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
split_version = re.split("^([0-9]+)\.([0-9]+)\.([0-9]+)(.*?)$", version)
major_version = int(split_version[1])

# For calculating tags
import github
gh = github.Github()
ome = "openmicroscopy"
scc = "snoopycrimecop"

repo1 = gh.get_organization(ome).get_repo(ome)
repo2 = gh.get_user(scc).get_repo(ome)

for repo in (repo1, repo2):
    found = False
    for tag in repo.get_tags():
        if tag.name == ("v.%s" % version):
            found = True
            break
    if found:
        break

repl["@TAG_URL@"] = repo.html_url + '/tree/' + tag.name
repl["@DOC_URL@"] = "https://www.openmicroscopy.org/site/support/omero%s" \
    % major_version
if "STAGING" in os.environ and os.environ.get("STAGING"):
    repl["@DOC_URL@"] += "-staging"

if "SNAPSHOT_PATH" in os.environ:
    SNAPSHOT_PATH = os.environ.get('SNAPSHOT_PATH')
else:
    SNAPSHOT_PATH = "/ome/data_repo/public/"

OMERO_SNAPSHOT_PATH = SNAPSHOT_PATH + "/omero/" + version + "/"

if "ANNOUCEMENT_URL" in os.environ:
    repl["@ANNOUCEMENT_URL@"] = os.environ.get('ANNOUCEMENT_URL')
else:
    repl["@ANNOUCEMENT_URL@"] = \
        "https://www.openmicroscopy.org/community/viewforum.php?f=11"

if "MILESTONE" in os.environ:
    repl["@MILESTONE@"] = os.environ.get('MILESTONE')
else:
    repl["@MILESTONE@"] = "OMERO-%s" % version

for x, y in (
        ("LINUX_CLIENTS",
         "artifacts/OMERO.clients-@VERSION@-ice35-@BUILD@.linux.zip"),
        ("MAC_CLIENTS",
         "artifacts/OMERO.clients-@VERSION@-ice35-@BUILD@.mac.zip"),
        ("WIN_CLIENTS",
         "artifacts/OMERO.clients-@VERSION@-ice35-@BUILD@.win.zip"),
        ("IJ_CLIENTS",
         "artifacts/OMERO.insight-ij-@VERSION@-ice35-@BUILD@.zip"),
        ("MATLAB_CLIENTS",
         "artifacts/OMERO.matlab-@VERSION@-ice35-@BUILD@.zip"),
        ("SERVER33", "artifacts/OMERO.server-@VERSION@-ice33-@BUILD@.zip"),
        ("SERVER34", "artifacts/OMERO.server-@VERSION@-ice34-@BUILD@.zip"),
        ("SERVER35", "artifacts/OMERO.server-@VERSION@-ice35-@BUILD@.zip"),
        ("DOCS", "artifacts/OMERO.docs-@VERSION@-ice33-@BUILD@.zip"),
        ("VM", "artifacts/OMERO.vm-@VERSION@-@BUILD@.ova"),
        ("DOC", "artifacts/OMERO-@VERSION@.pdf")):

    find_pkg(repl, fingerprint_url, OMERO_SNAPSHOT_PATH, x, y, MD5s)


for line in fileinput.input(["omero_downloads.html"]):
    print repl_all(repl, line, check_http=True),

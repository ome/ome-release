#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fileinput

from doc_generator import find_pkg, repl_all

fingerprint_url = "http://hudson.openmicroscopy.org.uk/fingerprint"
daily_url = "http://hudson.openmicroscopy.org.uk/job/BIOFORMATS-daily/" \
    "lastSuccessfulBuild/artifact/artifacts"
trunk_url = "http://hudson.openmicroscopy.org.uk/job/BIOFORMATS-trunk/" \
    "lastSuccessfulBuild/artifact/artifacts"


def usage():
    print "bfgen.py version"
    sys.exit(1)

try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

MD5s = []

# Read major version from input version
import re
split_version = re.split("^([0-9]+)\.([0-9]+)\.([0-9]+)(.*?)$", version)
major_version = int(split_version[1])

# For calculating tags
import github
gh = github.Github()
ome = "openmicroscopy"
scc = "snoopycrimecop"
bf = "bioformats"

repo1 = gh.get_organization(ome).get_repo(bf)
repo2 = gh.get_user(scc).get_repo(bf)

for repo in (repo1, repo2):
    found = False
    for tag in repo.get_tags():
        if tag.name == ("v%s" % version):
            found = True
            break
    if found:
        break

repl["@TAG_URL@"] = repo.html_url + '/tree/' + tag.name
repl["@DOC_URL@"] = \
    "http://www.openmicroscopy.org/site/support/bio-formats%s" \
    % major_version

if "SNAPSHOT_PATH" in os.environ:
    SNAPSHOT_PATH = os.environ.get('SNAPSHOT_PATH')
else:
    SNAPSHOT_PATH = "/ome/data_repo/public/"


BF_SNAPSHOT_PATH = SNAPSHOT_PATH + "/bio-formats/" + version + "/"

for x, y in (
        ("LOCI_TOOLS", "artifacts/loci_tools.jar"),
        ("OME_TOOLS", "artifacts/ome_tools.jar"),
        ("COMMAND_LINE_TOOLS", "artifacts/bftools.zip"),
        ("MATLAB_TOOLS", "artifacts/bfmatlab.zip"),
        ("bio-formats.jar", "artifacts/bio-formats.jar"),
        ("scifio.jar", "artifacts/scifio.jar"),
        ("ome-io.jar", "artifacts/ome-io.jar"),
        ("ome-xml.jar", "artifacts/ome-xml.jar"),
        ("ome_plugins.jar", "artifacts/ome_plugins.jar"),
        ("poi-loci.jar", "artifacts/poi-loci.jar"),
        ("jai_imageio.jar", "artifacts/jai_imageio.jar"),
        ("lwf-stubs.jar", "artifacts/lwf-stubs.jar"),
        ("mdbtools-java.jar", "artifacts/mdbtools-java.jar"),
        ("metakit.jar", "artifacts/metakit.jar"),
        ("loci-common.jar", "artifacts/loci-common.jar"),
        ("loci_plugins.jar", "artifacts/loci_plugins.jar"),
        ("loci-testing-framework.jar",
         "artifacts/loci-testing-framework.jar"),
        ("loci-legacy.jar", "artifacts/loci-legacy.jar"),
        ("scifio-devel.jar", "artifacts/scifio-devel.jar"),
        ("scifio-test.jar", "artifacts/scifio-test.jar"),
        ("specification.jar", "artifacts/specification.jar"),
        ("turbojpeg.jar", "artifacts/turbojpeg.jar"),
        ("DOC", "artifacts/Bio-Formats-@VERSION@.pdf")):

    find_pkg(repl, fingerprint_url, BF_SNAPSHOT_PATH, x, y, MD5s)

    repl["@DAILY_%s@" % x] = "%s/%s" % (daily_url, x)
    repl["@TRUNK_%s@" % x] = "%s/%s" % (trunk_url, x)

for line in fileinput.input(["bf_downloads.html"]):
    print repl_all(repl, line, check_http=True),

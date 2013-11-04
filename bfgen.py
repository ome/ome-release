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

# # Creating Github instance
# try:
#     p = subprocess.Popen("git","config","--get","github.token", stdout =
#                          subprocess.PIPE)
#     rc = p.wait()
#     if rc:
#         raise Exception("rc=%s" % rc)
#     token = p.communicate()
# except Exception:
#     token = None
#
# gh = github.Github(token, user_agent="PyGithub")
# repo = gh.get_organization("openmicroscopy").get_repo("bioformats")
# for tag in repo.get_tags():
#     if tag.name == ("v%s" % version):
#         break
# repl["@SHA1_FULL@"] = tag.commit.sha
# repl["@SHA1_SHORT@"] = tag.commit.sha[0:10]
repl["@DOC_URL@"] = \
    "https://www.openmicroscopy.org/site/support/bio-formats%s" \
    % major_version
if "STAGING" in os.environ and os.environ.get("STAGING"):
    repl["@DOC_URL@"] += "-staging"

if "SNAPSHOT_PATH" in os.environ:
    SNAPSHOT_PATH = os.environ.get('SNAPSHOT_PATH')
else:
    SNAPSHOT_PATH = "/ome/data_repo/public/"


BF_SNAPSHOT_PATH = SNAPSHOT_PATH + "/bio-formats/" + version + "/"

for x, y in (
        ("bio-formats.jar", "artifacts/bio-formats.jar"),
        ("scifio.jar", "artifacts/scifio.jar"),
        ("bftools.zip", "artifacts/bftools.zip"),
        ("bfmatlab.zip", "artifacts/bfmatlab.zip"),
        ("ome_tools.jar", "artifacts/ome_tools.jar"),
        ("ome-io.jar", "artifacts/ome-io.jar"),
        ("ome-xml.jar", "artifacts/ome-xml.jar"),
        ("ome_plugins.jar", "artifacts/ome_plugins.jar"),
        ("poi-loci.jar", "artifacts/poi-loci.jar"),
        ("jai_imageio.jar", "artifacts/jai_imageio.jar"),
        ("lwf-stubs.jar", "artifacts/lwf-stubs.jar"),
        ("mdbtools-java.jar", "artifacts/mdbtools-java.jar"),
        ("metakit.jar", "artifacts/metakit.jar"),
        ("loci-common.jar", "artifacts/loci-common.jar"),
        ("loci_tools.jar", "artifacts/loci_tools.jar"),
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

for line in fileinput.input(["bftmpl.txt"]):
    print repl_all(repl, line, check_http=True),

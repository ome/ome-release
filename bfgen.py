#!/usr/bin/env python
# -*- coding: utf-8 -*-

import github
import subprocess
from doc_generator import *

fingerprint_url = "http://hudson.openmicroscopy.org.uk/fingerprint"
daily_url = "http://hudson.openmicroscopy.org.uk/job/BIOFORMATS-daily/lastSuccessfulBuild/artifact/artifacts"
trunk_url = "http://hudson.openmicroscopy.org.uk/job/BIOFORMATS-trunk/lastSuccessfulBuild/artifact/artifacts"


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
split_version =  re.split("^([0-9]+)\.([0-9]+)\.([0-9]+)(.*?)$", version)
major_version = int(split_version[1])

# # Creating Github instance
# try:
#     p = subprocess.Popen("git","config","--get","github.token", stdout = subprocess.PIPE)
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
repl["@DOC_URL@"] = "https://www.openmicroscopy.org/site/support/bio-formats%s" % major_version
if "STAGING" in os.environ and os.environ.get("STAGING"):
    repl["@DOC_URL@"] += "-staging"

if "SNAPSHOT_PATH" in os.environ:
    SNAPSHOT_PATH =  os.environ.get('SNAPSHOT_PATH')
else:
    SNAPSHOT_PATH = "/ome/data_repo/public/"


BF_SNAPSHOT_PATH = SNAPSHOT_PATH + "/bio-formats/"

for x, y in (
    ("bio-formats.jar", "@VERSION@/bio-formats.jar"),
    ("scifio.jar", "@VERSION@/scifio.jar"),
    ("bftools.zip", "@VERSION@/bftools.zip"),
    ("bfmatlab.zip", "@VERSION@/bfmatlab.zip"),
    ("ome_tools.jar", "@VERSION@/ome_tools.jar"),
    ("ome-io.jar", "@VERSION@/ome-io.jar"),
    ("ome-xml.jar", "@VERSION@/ome-xml.jar"),
    ("ome_plugins.jar", "@VERSION@/ome_plugins.jar"),
    ("ome-editor.jar", "@VERSION@/ome-editor.jar"),
    ("poi-loci.jar", "@VERSION@/poi-loci.jar"),
    ("jai_imageio.jar", "@VERSION@/jai_imageio.jar"),
    ("lwf-stubs.jar", "@VERSION@/lwf-stubs.jar"),
    ("mdbtools-java.jar", "@VERSION@/mdbtools-java.jar"),
    ("metakit.jar", "@VERSION@/metakit.jar"),
    ("loci-common.jar", "@VERSION@/loci-common.jar"),
    ("loci_tools.jar", "@VERSION@/loci_tools.jar"),
    ("loci_plugins.jar", "@VERSION@/loci_plugins.jar"),
    ("loci-testing-framework.jar", "@VERSION@/loci-testing-framework.jar"),
    ("DOC", "@VERSION@/Bio-Formats-@VERSION@.pdf")
    ):

    find_pkg(repl, fingerprint_url, BF_SNAPSHOT_PATH, x, y, MD5s)

    repl["@DAILY_%s@" % x] = "%s/%s" % (daily_url, x)
    repl["@TRUNK_%s@" % x] = "%s/%s" % (trunk_url, x)

for line in fileinput.input(["bftmpl.txt"]):
    print repl_all(repl, line, check_http=True),

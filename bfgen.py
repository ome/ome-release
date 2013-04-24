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

# Creating Github instance
try:
    p = subprocess.Popen("git","config","--get","github.token", stdout = subprocess.PIPE)
    rc = p.wait()
    if rc:
        raise Exception("rc=%s" % rc)
    token = p.communicate()
except Exception:
    token = None

gh = github.Github(token, user_agent="PyGithub")
org = gh.get_organization("openmicroscopy")
repo = org.get_repo("openmicroscopy")
for tag in repo.get_tags():
    if tag.name == ("v.%s" % version):
        break
repl["@SHA1_FULL@"] = tag.commit.sha
repl["@SHA1_SHORT@"] = tag.commit.sha[0:10]
if "STAGING" in os.environ:
    repl["@DOC_URL@"] = "https://www.openmicroscopy.org/site/support/bio-formats-staging"
else:
    repl["@DOC_URL@"] = "https://www.openmicroscopy.org/site/support/bio-formats"
repl["@PDF_URL@"] = repl["@DOC_URL@"] + "/Bio-Formats-%s.pdf" % version

if "SNAPSHOT_PATH" in os.environ:
    SNAPSHOT_PATH =  os.environ.get('SNAPSHOT_PATH')
else:
    SNAPSHOT_PATH = "/var/www/cvs.openmicroscopy.org.uk/snapshots"

if "SNAPSHOT_URL" in os.environ:
    SNAPSHOT_URL =  os.environ.get('SNAPSHOT_URL')
else:
    SNAPSHOT_URL = "http://cvs.openmicroscopy.org.uk/snapshots"

BF_SNAPSHOT_PATH = SNAPSHOT_PATH + "/bioformats/"
BF_SNAPSHOT_URL = SNAPSHOT_URL + "/bioformats/"
repl["@SNAPSHOT_URL@"] = SNAPSHOT_URL


for x in ["bio-formats.jar", "scifio.jar", "bftools.zip",
         "ome_tools.jar", "ome-io.jar", "ome-xml.jar", "ome_plugins.jar", "ome-editor.jar",
         "poi-loci.jar", "jai_imageio.jar", "lwf-stubs.jar", "mdbtools-java.jar", "metakit.jar",
         "loci-common.jar", "loci_tools.jar", "loci_plugins.jar", "loci-testing-framework.jar"]:

    find_pkg(repl, fingerprint_url, BF_SNAPSHOT_PATH, BF_SNAPSHOT_URL, \
            x, "@VERSION@/%s" % x, MD5s)

    repl["@DAILY_%s@" % x] = "%s/%s" % (daily_url, x)
    repl["@TRUNK_%s@" % x] = "%s/%s" % (trunk_url, x)

for line in fileinput.input(["bftmpl.txt"]):
    print repl_all(repl, line, check_http=True),

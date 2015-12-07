#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fileinput

from utils import RSYNC_PATH, get_version, get_tag_url
from doc_generator import find_pkg, repl_all


def usage():
    print "bfcppgen.py version"
    sys.exit(1)

try:
    version = sys.argv[1]
except:
    usage()

repl = {"@VERSION@": version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y")}

# Read major and minor version from input version
major_version, minor_version = get_version(version)

repl["@TAG_URL@"] = get_tag_url("bioformats", version)
repl["@SUPERBUILD_TAG_URL@"] = get_tag_url("ome-cmake-superbuild",
                                           version, org="ome")
repl["@DOC_URL@"] = (
    "http://www.openmicroscopy.org/site/support/bio-formats%s.%s"
    % (major_version, minor_version))

PREFIX = os.environ.get('PREFIX', 'bio-formats-cpp')
BFCPP_RSYNC_PATH = '%s/%s/%s/' % (RSYNC_PATH, PREFIX, version)

# Links to Bio-Formats artifacts
BF_RELATIVE_PATH = '../../bio-formats/@VERSION@/artifacts/'
bf_artifacts = [
    ("DOC", BF_RELATIVE_PATH + "/Bio-Formats-@VERSION@.pdf"),
    ("SOURCE_CODE", BF_RELATIVE_PATH + "bioformats-@VERSION@.zip")]

# Links to Bio-Formats C++ artifacts
platforms = {'UBUNTU1404': 'Ubuntu14.04-x86_64',
             'OSX1011':    'MacOSX10.11-x86_64',
             'OSX1010':    'MacOSX10.10-x86_64',
             'OSX109':     'MacOSX10.9-x86_64',
             'CENTOS66':   'CentOS6.6-x86_64',
             'CENTOS71':   'CentOS7.1-x86_64',
             'FREEBSD102': 'FreeBSD10.2-amd64'}

win_platforms = {'WINDOWSVC12X64': 'WindowsVC12-x64',
                 'WINDOWSVC12X86': 'WindowsVC12-x86'}

build_types = ['Debug', 'Release']

bf_cpp_artifacts = [
    ("DOXYGEN", "artifacts/bioformats-cpp-apidoc-@VERSION@.tar.xz"),
    ("SUPERBUILD_SOURCE_CODE",
     "artifacts/ome-cmake-superbuild-@VERSION@.tar.xz")]

for platform in platforms.keys():
    for build_type in build_types:
        bf_cpp_artifacts.append(
            ('%s_%s' % (platform, build_type.upper()),
             'artifacts/superbuild/bioformats-cpp-@VERSION@-%s-%s.tar.xz'
             % (build_type, platforms[platform])))
for platform in win_platforms.keys():
    for build_type in build_types:
        bf_cpp_artifacts.append(
            ('%s_%s' % (platform, build_type.upper()),
             'artifacts/superbuild/bioformats-cpp-@VERSION@-%s-%s.zip'
             % (build_type, win_platforms[platform])))

bf_cpp_platform_artifacts = list()
for platform in platforms.keys():
    for build_type in build_types:
        platform_artifact = \
            ('%sPLATFORM_%s' % (platform, build_type.upper()),
             'artifacts/platform/bioformats-cpp-@VERSION@-%s-%s.tar.xz'
             % (build_type, platforms[platform]))
        try:
            find_pkg(repl, BFCPP_RSYNC_PATH,
                     platform_artifact[0], platform_artifact[1])
            bf_cpp_artifacts.append(platform_artifact)
        except:
            pass

for x, y in bf_artifacts + bf_cpp_artifacts:
    find_pkg(repl, BFCPP_RSYNC_PATH, x, y)

for line in fileinput.input(["bf_cpp_downloads.html"]):
    print repl_all(repl, line, check_http=True)

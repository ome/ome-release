#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import fileinput

from utils import RSYNC_PATH, get_tag_url
from doc_generator import find_pkg, repl_all


def usage():
    print "filescppgen.py files_version buildid"
    sys.exit(1)


try:
    files_job_version = sys.argv[1]
    buildid = sys.argv[2]
except:
    usage()

superbuild_version = '0.3.0'
common_version = '5.4.0'
model_version = '5.5.0'
files_version = '0.3.0'
qtwidgets_version = '5.4.0'

if files_job_version != files_version:
    print "files version mismatch"
    sys.exit(1)

repl = {"@VERSION@": files_version,
        "@BUILDID@": buildid,
        "@MODEL_VERSION@": model_version,
        "@COMMON_VERSION@": common_version,
        "@FILES_VERSION@": files_version,
        "@QTWIDGETS_VERSION@": qtwidgets_version,
        "@SUPERBUILD_VERSION@": superbuild_version,
        "@MONTHYEAR@": datetime.datetime.now().strftime("%b %Y"),
        "@YEAR@": datetime.datetime.now().strftime("%Y")}

repl["@SUPERBUILD_TAG_URL@"] = get_tag_url("ome-cmake-superbuild",
                                           superbuild_version,
                                           org="ome")
repl["@COMMON_TAG_URL@"] = get_tag_url("ome-common-cpp",
                                       common_version, org="ome")
repl["@MODEL_TAG_URL@"] = get_tag_url("ome-model", model_version,
                                      org="ome")
repl["@FILES_TAG_URL@"] = get_tag_url("ome-files-cpp",
                                      files_version, org="ome")
repl["@QTWIDGETS_TAG_URL@"] = get_tag_url("ome-qtwidgets",
                                          qtwidgets_version,
                                          org="ome")

repl["@DOC_URL@"] = (
    "docs/ome-files-bundle-docs-%s-b%s/" %
    (files_version, buildid))
repl["@DOC_FILES_URL@"] = (
    "docs/ome-files-bundle-docs-%s-b%s/ome-files/manual/html/" %
    (files_version, buildid))
repl["@DOC_SUPERBUILD_URL@"] = (
    "docs/ome-files-bundle-docs-%s-b%s/"
    "ome-cmake-superbuild/manual/html/" % (files_version, buildid))
repl["@COMMON_API_URL@"] = (
    "docs/ome-files-bundle-docs-%s-b%s/ome-common/api/html/" %
    (files_version, buildid))
repl["@XML_API_URL@"] = (
    "docs/ome-files-bundle-docs-%s-b%s/ome-xml/api/html/" %
    (files_version, buildid))
repl["@FILES_API_URL@"] = (
    "docs/ome-files-bundle-docs-%s-b%s/ome-files/api/html/" %
    (files_version, buildid))

PREFIX = os.environ.get('PREFIX', 'ome-files-cpp')
FILESCPP_RSYNC_PATH = '%s/%s/%s/%s/' % (RSYNC_PATH, PREFIX,
                                        files_version, buildid)

# Links to source releases
RELATIVE_PATH = '../../../'
ome_sources = [
    ("COMMON_SOURCE_TXZ", RELATIVE_PATH +
     ("ome-common-cpp/%s/source/" +
      "ome-common-cpp-%s.tar.xz") % (
          common_version, common_version)),
    ("COMMON_SOURCE_ZIP", RELATIVE_PATH +
     ("ome-common-cpp/%s/source/" +
      "ome-common-cpp-%s.zip") % (
          common_version, common_version)),
    ("MODEL_SOURCE_TXZ", RELATIVE_PATH +
     ("ome-model/%s/source/" +
      "ome-model-%s.tar.xz") % (
          model_version, model_version)),
    ("MODEL_SOURCE_ZIP", RELATIVE_PATH +
     ("ome-model/%s/source/" +
      "ome-model-%s.zip") % (
          model_version, model_version)),
    ("FILES_SOURCE_TXZ", RELATIVE_PATH +
     ("ome-files-cpp/%s/source/" +
      "ome-files-cpp-%s.tar.xz") % (
          files_version, files_version)),
    ("FILES_SOURCE_ZIP", RELATIVE_PATH +
     ("ome-files-cpp/%s/source/" +
      "ome-files-cpp-%s.zip") % (
          files_version, files_version)),
    ("QTWIDGETS_SOURCE_TXZ", RELATIVE_PATH +
     ("ome-qtwidgets/%s/source/" +
      "ome-qtwidgets-%s.tar.xz") % (
          qtwidgets_version, qtwidgets_version)),
    ("QTWIDGETS_SOURCE_ZIP", RELATIVE_PATH +
     ("ome-qtwidgets/%s/source/" +
      "ome-qtwidgets-%s.zip") % (
          qtwidgets_version, qtwidgets_version)),
    ("SUPERBUILD_SOURCE_TXZ", RELATIVE_PATH +
     ("ome-cmake-superbuild/%s/source/" +
      "ome-cmake-superbuild-%s.tar.xz") % (
          superbuild_version, superbuild_version)),
    ("SUPERBUILD_SOURCE_ZIP", RELATIVE_PATH +
     ("ome-cmake-superbuild/%s/source/" +
      "ome-cmake-superbuild-%s.zip") % (
          superbuild_version, superbuild_version))]

thirdparty_sources = {
    'BOOST_SOURCE': 'boost_1_63_0.tar.bz2',
    'BZIP2_SOURCE': 'bzip2-1.0.6.tar.gz',
    'GTEST_SOURCE': 'release-1.8.0.tar.gz',
    'ICU_SOURCE': 'icu4c-57_1-src.tgz',
    'PNG_SOURCE': 'libpng-1.6.28.tar.xz',
    'TIFF_SOURCE': 'tiff-4.0.7.tar.gz',
    'XALAN_SOURCE': 'xalan_c-1.11-src.tar.gz',
    'XERCES_SOURCE': 'xerces-c-3.1.4.tar.xz',
    'ZLIB_SOURCE': 'zlib-1.2.10.tar.xz'}

thirdparty_tools = {
    'PATCH_SOURCE': 'patch-2.5.9-7-bin.zip',
    'PY_DOCUTILS_SOURCE': 'docutils-0.12.tar.gz',
    'PY_GENSHI_SOURCE': 'Genshi-0.7.tar.gz',
    'PY_JINJA2_SOURCE': 'Jinja2-2.7.3.tar.gz',
    'PY_MARKUPSAFE_SOURCE': 'MarkupSafe-0.23.tar.gz',
    'PY_PYGMENTS_SOURCE': 'Pygments-2.0.2.tar.gz',
    'PY_SETUPTOOLS_SOURCE': 'setuptools-18.3.2.tar.gz',
    'PY_SPHINX_SOURCE': 'Sphinx-1.2.3.tar.gz',
    'TOFRODOS_SOURCE': 'tfd1713.zip'}

# Links to Bio-Formats C++ binaries
platforms = {'UBUNTU1404': 'Ubuntu14.04-x86_64',
             'OSX1012':    'MacOSX10.12.2-x86_64',
             'FREEBSD11':  'FreeBSD11.0-amd64',
             'CENTOS68':   'CentOS6.8-x86_64',
             'CENTOS72':   'CentOS7.3-x86_64'}

win_platforms = {'WINDOWSVC12X64': 'VC12-x64',
                 'WINDOWSVC12X86': 'VC12-x86',
                 'WINDOWSVC14X64': 'VC14-x64',
                 'WINDOWSVC14X86': 'VC14-x86'}

build_types = ['Debug', 'Release']

files_cpp_artifacts = [
    ("DOCS_BUNDLE_TAR",
     "docs/ome-files-bundle-docs-%s-b%s.tar.xz" %
     (files_version, buildid)),
    ("DOCS_BUNDLE_ZIP",
     "docs/ome-files-bundle-docs-%s-b%s.zip" %
     (files_version, buildid))]

for platform in platforms.keys():
    for build_type in build_types:
        files_cpp_artifacts.append(
            ('%s_%s' % (platform, build_type.upper()),
             'binaries/' +
             'ome-files-standalone-bundle-%s-%s-%s-b%s.tar.xz'
             % (files_version, build_type, platforms[platform],
                buildid)))
for platform in win_platforms.keys():
    for build_type in build_types:
        files_cpp_artifacts.append(
            ('%s_%s' % (platform, build_type.upper()),
             'binaries/' +
             'ome-files-bundle-%s-%s-%s-b%s.zip'
             % (files_version, win_platforms[platform],
                build_type, buildid)))

files_cpp_platform_artifacts = list()
for platform in platforms.keys():
    for build_type in build_types:
        platform_artifact = \
            ('%sPLATFORM_%s' % (platform, build_type.upper()),
             'binaries/' +
             'ome-files-platform-bundle-%s-%s-%s-b%s.tar.xz'
             % (files_version, build_type, platforms[platform],
                buildid))
        try:
            find_pkg(repl, FILESCPP_RSYNC_PATH,
                     platform_artifact[0], platform_artifact[1])
            files_cpp_artifacts.append(platform_artifact)
        except:
            pass

for src in thirdparty_sources.keys():
    files_cpp_artifacts.append(
        (src,
         'sources/%s' % (thirdparty_sources[src])))
for src in thirdparty_tools.keys():
    files_cpp_artifacts.append(
        (src,
         'tools/%s' % (thirdparty_tools[src])))

for x, y in ome_sources + files_cpp_artifacts:
    find_pkg(repl, FILESCPP_RSYNC_PATH, x, y)

for line in fileinput.input(["files_cpp_downloads.html"]):
    print repl_all(repl, line, check_http=True)

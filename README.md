OME release scripts
==================

These scripts are used during the OMERO release to copy the build
artifacts to cvs.openmicroscopy.org and generate the
[OMERO](http://www.openmicroscopy.org/site/products/omero/downloads) and
[Bio-Formats](http://www.openmicroscopy.org/site/products/bio-formats/downloads)
download pages for each release.

Prerequisites
-------------

* Merge all PRs related to the upcoming release. Update all submodules using the OMERO-submods-{stable, develop} jobs.

* Tag the `RELEASE` of openmicroscopy.git and bioformats.git

	```
	git tag -u "Josh Moore (Glencoe Software, Inc.) <you@example.com>" -m "Release version RELEASE" v.RELEASE
	````

* Push the tag and the branch to GitHub

	```
	git push origin v.RELEASE develop
	```

* After the BIOFORMATS-{stable, trunk}, OMERO-{stable,trunk} and
OMERO-{stable,trunk}-ice34 builds pass, promote them. This will transfer the
build artifacts to $ARTIFACT_PATH/$BUILD_NAME/$BUILD_NUMBER.

Preparation
-----------

Run [prep.sh](prep.sh) as hudson. This script performs the following actions:

- Create two folders for symlinking the artifacts under `SNAPSHOT_PATH`: `omero/RELEASE` and `bioformats/RELEASE`

- Symlink all the promoted OMERO artifacts to `omero/RELEASE/`

- Rename the OVA to include the version number (e.g. RELEASE) and be sure to
modify the MD5 file to use the new name.

- Symlink all the promoted Bio-Formats artifacts to `bioformats/RELEASE/`

Several environment variables can be configured for this step:

- `RELEASE` is the number of the upcoming release for example 4.4.7

- `OMERO_JOB`, `OMERO_ICE34_JOB` and `BIOFORMATS_JOB` determine the names of
the jobs used to produce the release artifacts, for example OMERO-stable,
OMERO-stable-ice34 and BIOFORMATS-stable.

- `OMERO_BUILD`, `OMERO_ICE34_BUILD` and `BIOFORMATS_BUILD` determine the
build numbers of the jobs used to produce the release artifacts.

- `VIRTUALBOX_PATH` and `ARTIFACT_PATH` are the folders where the OVA and the
promoted builds are stored. Their default values are /ome/data_repo/virtualbox
and /ome/data_repo/releases.

- `SNAPSHOT_PATH` is the folder where the OMERO and Bio-Formats artifacts will
be symlinked. Its default value is
/var/www/cvs.openmicroscopy.org.uk/snapshots.

Downloads page generation
-------------------------

* To generate the OMERO downloads page, run [gen.py](gen.py):

	```
	python gen.py RELEASE bBUILDNUMBER [bBUILDNUMBER_ICE34]
	```

  If the Ice 3.4 build number is not specified, it is assumed to be the same
  as the Ice 3.3 build number

* To generate the Bio-Formats downloads page, run [bfgen.py](bfgen.py):

	```
     python bfgen.py RELEASE bBUILDNUMBER
	```

Several environment variables can be configured for this step:

- if `STAGING` is defined, the documentation URL will point at the staging
documentation instead of the release documentation, for example
https://www.openmicroscopy.org/site/support/bio-formats-staging instead of
https://www.openmicroscopy.org/site/support/bio-formats.

- `SNAPSHOT_PATH` and `SNAPSHOT_URL` are the folder and the URL where the
OMERO and Bio-Formats artifacts are symlinked and downloadable. Their default
values are /var/www/cvs.openmicroscopy.org.uk/snapshots and
http://cvs.openmicroscopy.org.uk/snapshots.

- `ANNOUCEMENT_URL` is the URL of the announcement post to be used in the
OMERO downloads page.

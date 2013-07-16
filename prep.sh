#!/bin/bash

set -e
set -u
set -x

FAIL_ON_DUPLICATES=${FAIL_ON_DUPLICATES:-True}
RELEASE=${RELEASE:-}
OMERO_BUILD=${OMERO_BUILD:-}
OMERO_ICE34_BUILD=${OMERO_ICE34_BUILD:-${OMERO_BUILD}}
OMERO_VIRTUALBOX_BUILD=${OMERO_VIRTUALBOX_BUILD:-${OMERO_BUILD}}
BIOFORMATS_BUILD=${BIOFORMATS_BUILD:-}
OMERO_JOB=${OMERO_JOB:-OMERO-stable}
OMERO_ICE34_JOB=${OMERO_ICE34_JOB:-$OMERO_JOB-ice34}
OMERO_VIRTUALBOX_JOB=${OMERO_VIRTUALBOX_JOB:-$OMERO_JOB-virtualbox}
BIOFORMATS_JOB=${BIOFORMATS_JOB:-BIOFORMATS-stable}
VIRTUALBOX_PATH=${VIRTUALBOX_PATH:-/ome/data_repo/virtualbox}
ARTIFACT_PATH=${ARTIFACT_PATH:-/ome/data_repo/releases}
SNAPSHOT_PATH=${SNAPSHOT_PATH:-/var/www/cvs.openmicroscopy.org.uk/snapshots}

# Test artifact directory existence
if [[ -z $OMERO_BUILD ]] ; then
    echo "Not releasing OMERO"
else
    echo "Checking OMERO artifacts"
    OMERO_ARTIFACT_PATH=$ARTIFACT_PATH/$OMERO_JOB/$OMERO_BUILD
    [[ -d $OMERO_ARTIFACT_PATH ]] || exit
    OMERO_ICE34_ARTIFACT_PATH=$ARTIFACT_PATH/$OMERO_ICE34_JOB/$OMERO_ICE34_BUILD
    [[ -d $OMERO_ICE34_ARTIFACT_PATH ]] || exit
    OMERO_VIRTUALBOX_ARTIFACT_PATH=$ARTIFACT_PATH/$OMERO_VIRTUALBOX_JOB/$OMERO_VIRTUALBOX_BUILD
    [[ -d $OMERO_VIRTUALBOX_ARTIFACT_PATH ]] || exit
fi

if [[ -z $BIOFORMATS_BUILD ]]; then
    echo "Not releasing Bio-Formats"
else
    echo "Checking Bio-Formats artifacts"
    BIOFORMATS_ARTIFACT_PATH=$ARTIFACT_PATH/$BIOFORMATS_JOB/$BIOFORMATS_BUILD
    [[ -d $BIOFORMATS_ARTIFACT_PATH ]] || exit
fi

# Create OMERO & Bio-Formats directories
if [[ !  -z $OMERO_BUILD ]]; then
    echo "Creating OMERO release directories"
    OMERO_SNAPSHOT_PATH=$SNAPSHOT_PATH/omero
    [[ -d $OMERO_SNAPSHOT_PATH ]] ||  mkdir $OMERO_SNAPSHOT_PATH
    OMERO_VIRTUALBOX_PATH=$OMERO_SNAPSHOT_PATH/virtualbox
    [[ -d $OMERO_VIRTUALBOX_PATH ]] ||  mkdir $OMERO_VIRTUALBOX_PATH

    # Create OMERO release directory
    OMERO_RELEASE_PATH=$OMERO_SNAPSHOT_PATH/$RELEASE
    if [[ -d $OMERO_RELEASE_PATH ]]
    then
        echo "$OMERO_RELEASE_PATH already exists"
        [ $FAIL_ON_DUPLICATES ] && exit
    else
        mkdir $OMERO_RELEASE_PATH
    fi
fi

if [[ ! -z $BIOFORMATS_BUILD ]]; then
    echo "Creating Bio-Formats release directories"
    BIOFORMATS_SNAPSHOT_PATH=$SNAPSHOT_PATH/bioformats
    [[ -d $BIOFORMATS_SNAPSHOT_PATH ]] ||  mkdir $BIOFORMATS_SNAPSHOT_PATH

    # Create Bio-Formats release directory
    BIOFORMATS_RELEASE_PATH=$BIOFORMATS_SNAPSHOT_PATH/$RELEASE
    if [[ -d $BIOFORMATS_RELEASE_PATH ]]
    then
        echo "$BIOFORMATS_RELEASE_PATH already exists"
        [ $FAIL_ON_DUPLICATES ] && exit
    else
        mkdir $BIOFORMATS_RELEASE_PATH
    fi
fi

# Symlink artifacts into release directories
if [[ ! -z $OMERO_BUILD ]]; then
    echo "Symlinking OMERO artifacts"
    for x in $OMERO_ARTIFACT_PATH/*;
        do ln -sf "$x" "$OMERO_RELEASE_PATH/";
    done
    for x in $OMERO_ICE34_ARTIFACT_PATH/*;
        do ln -sf "$x" "$OMERO_RELEASE_PATH/";
    done
    for x in $OMERO_VIRTUALBOX_ARTIFACT_PATH/*;
        do ln -sf "$x" "$OMERO_VIRTUALBOX_PATH/";
    done
fi

if [[ ! -z $BIOFORMATS_BUILD ]]; then
    echo "Symlinking Bio-Formats artifacts"
    for x in $BIOFORMATS_ARTIFACT_PATH/*;
        do ln -sf "$x" "$BIOFORMATS_RELEASE_PATH/";
    done
fi

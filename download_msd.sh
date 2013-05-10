#!/usr/bin/env bash

DATA=data/
MSD_SITE="http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles"

mkdir -p $DATA

# Download MSD Summary file for Tempo Histogram. 300 MB file.
wget -p $DATA $MSD_SITE/msd_summary_file.h5

# Download Track Metadata SQLite DB for Duration Histogram. 750 MB file.
wget -p $DATA $MSD_SITE/track_metadata.db

# Download list of tracks with year information for tempo_v_time and volume_v_time
wget -p $DATA $MSD_SITE/tracks_per_year.txt

unset DATA
unset MSD_SITE
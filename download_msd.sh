#!/usr/bin/env bash

DATA=data
MSD_SITE="http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles"

mkdir -p $DATA
mkdir -p $DATA/graphs

## Download data for Lyrics Analysis

wget -P $DATA $MSD_SITE/mxm_dataset_train.txt.zip
wget -P $DATA $MSD_SITE/mxm_dataset_test.txt.zip

unzip -d $DATA $DATA/mxm_dataset_train.txt.zip
unzip -d $DATA $DATA/mxm_dataset_test.txt.zip

cat $DATA/mxm_dataset_train.txt <(sed '1,18d' $DATA/mxm_dataset_test.txt) > $DATA/mxm.txt

rm $DATA/mxm_dataset_train.txt.zip
rm $DATA/mxm_dataset_test.txt.zip
rm $DATA/mxm_dataset_train.txt
rm $DATA/mxm_dataset_test.txt

## Download data for Duration, Volume, and Tempo Analysis

# Download MSD Summary file for Tempo Histogram. 300 MB file.
wget -P $DATA $MSD_SITE/msd_summary_file.h5

# Download Track Metadata SQLite DB for Duration Histogram. 750 MB file.
wget -P $DATA $MSD_SITE/track_metadata.db

# Download list of tracks with year information for tempo_v_time and volume_v_time
wget -P $DATA $MSD_SITE/tracks_per_year.txt

unset DATA
unset MSD_SITE
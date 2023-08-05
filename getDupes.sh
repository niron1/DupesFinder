#!/bin/bash

sudo python getFilesHashes.py / /tmp/filesHashesAndNames.txt 

awk -F"," '{print $1}'  /tmp/filesHashesAndNames.txt  | sort | uniq -d > /tmp/dupeHashes.txt

python getDupeFilenames.py /tmp/dupeHashes.txt /tmp/filesHashesAndNames.txt  /tmp/duplicates.txt

echo "Finished. list in /tmp/duplicates.txt"


#!/bin/bash
# A script to install requirements and generate data

echo "1/ Install requirements"
echo "---------------------------"
# Update Ubuntu packet manager
apt-get update -y
# INstall nano to easily debug scripts
apt-get install nano -y
# Install python (3.5)
apt-get install python3-pip -y

echo "2/ Generate datasets:"
echo "---------------------------"
cd SPAPS_BE2/utils

echo 'Generate text file'
python3 random_word_generator.py

# Go back to home dir
cd
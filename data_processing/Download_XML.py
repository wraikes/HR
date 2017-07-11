#!/usr/bin/python3
"""
Created on Thu Apr 13 10:00:13 2017

This program opens up the appropriate links to download the horse racing
XML files.  (Unfortunately, there is currently a blocker in place
to prevent automation).  After the downloads are complete, the program
will unzip and place the files in their appropriate directories.

@author: wraikes
"""

import webbrowser, zipfile, os, shutil, re, time

os.chdir('/home/wraikes/Downloads')

pps_re = re.compile(".+XML.xml$")
results_re = re.compile('.+tch.xml$')
zip_re = re.compile('.+ppsxml.zip$')
results_dir = '/home/wraikes/Programming/Personal_Projects/HorseRacing/Data/xml/results'
pps_dir = '/home/wraikes/Programming/Personal_Projects/HorseRacing/Data/xml/pp'

webbrowser.open('https://www.trackmaster.com/products/tch/samples')
webbrowser.open('https://www.trackmaster.com/products/tpp/samples')

time.sleep(20)

while True:
    _continue = input('Press ENTER when files are downloaded.')
    if _continue == '':
        break

for zip_file in os.listdir():
    if zip_re.search(zip_file):
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall()
        os.remove(zip_file)

for file in os.listdir():
    if results_re.search(file):
        shutil.move(file, results_dir)

    elif pps_re.search(file):
        shutil.move(file, pps_dir)
            

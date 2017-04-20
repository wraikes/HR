#!/usr/bin/python3

'''
Merge the processed pp and results DataFrames.

@author: wraikes
'''

import os


import data_processing.pp_process, data_processing.results_process


test = "nyc    10\nnyc    20"


salesMax = 0
oldKey = None

for line in test:
    data_mapped = line.strip().split('\t')
    
    thisKey, thisSale = data_mapped
    
    if oldKey and oldKey != thisKey:
        print oldKey, '\t', salesMax
        salesMax = 0
    
    oldKey = thisKey
    
    if thisSale > salesMax:
        salesMax = thisSale
    
if oldKey != None:
    print oldKey, '\t', salesMax














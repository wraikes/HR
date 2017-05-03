#!/usr/bin/python3

'''
Merge the processed pp and results DataFrames.

@author: wraikes
'''

import os
os.chdir('/home/wraikes/Programming/Personal_Projects/HorseRacing/Code/')

from data_processing.pp_process import *
from data_processing.results_process import *

file_pp = '/home/wraikes/Programming/Personal_Projects/HorseRacing/Data/xml/pp'
pp = xml_transform_pp(file_pp)

file_results = '/home/wraikes/Programming/Personal_Projects/HorseRacing/Data/xml/results'
results = xml_transform_results(file_results)

hr_df = pp.merge(results, how = 'left', on = ['horse_name', 'race_date', 'race', 'track'])
del pp, results

###Run cleaning script



hr_df.to_csv('/home/wraikes/Programming/Personal_Projects/HorseRacing/Data/data_files/HR_DF.csv')












#!/usr/bin/python3

'''
Compile and parse the past performances (pp) XML files into a pandas
DataFrame object.

@author: wraikes
'''

import os, xml.etree.ElementTree as eTree, pandas as pd

file_pp = r'C:\Users\LENOVO\Desktop\Academic\horseracing\Data\xml\pp'

def xml_transform_pp(directory):
    os.chdir(directory)
    races_for_df = []

    for file in os.listdir():

        if file.endswith('.xml'):
            root = eTree.parse(file).getroot()
            races_for_df += root_data(root)

    return pd.DataFrame(races_for_df)

def root_data(root):
    root_data_repo = []
    
    for race_no in root:
        race_no_stats = {}
      
        for child in race_no:
         
            if child.tag != 'horsedata':
                race_no_stats.update({child.tag: child.text})
                #root_data_repo.update({child.tag: child.text})
            else:
                horse_stats = race_no_stats.copy()
                horse_stats.update(horsedata(child))
                root_data_repo.append(horse_stats)
    
    return root_data_repo

def horsedata(parent):
    horsedata_repo = {}
    count_wo = 1
    count_pp = 1    
    tags = ['stats_data', 'jockey', 'trainer', 'workoutdata', 'ppdata']

    for child in parent:
        if child.tag not in tags:
            horsedata_repo.update({child.tag: child.text})       

        #Omitting stats_data because of too much missing data.
        elif child.tag == tags[0]:
            continue            
            
        elif child.tag == tags[1]:
            horsedata_repo.update(jockey(child))

        elif child.tag == tags[2]:
            horsedata_repo.update(trainer(child))

        elif child.tag == tags[3]:
            horsedata_repo.update(workoutdata(child, count_wo))
            count_wo += 1

        else:
            horsedata_repo.update(ppdata(child, count_pp))
            count_pp += 1
        
    return horsedata_repo

def jockey(parent):
    jockey_repo = {}

    for child in parent:
        if list(child) == []:
            jockey_repo.update({'J_' + child.tag: child.text})
        else:
            #potential bug if more than one stats data for jockey
            for grandchild in child[0]:
                jockey_repo.update({'J_SD_Last30_' + grandchild.tag: grandchild.text})

    return jockey_repo

def trainer(parent):
    trainer_repo = {}

    for child in parent:
        if list(child) == []:
            trainer_repo.update({'T_' + child.tag: child.text})
        else:
            #potential bug if more than one stats data for jockey
            for grandchild in child[0]:
                trainer_repo.update({'T_SD_Last30_' + grandchild.tag: grandchild.text})

    return trainer_repo

def workoutdata(parent, count):
    workout_repo = {}

    for child in parent:
        workout_repo.update({'WO_' + str(count) + '_' + child.tag: child.text})

    return workout_repo

def ppdata(parent, count):
    pp_repo = {}

    for child in parent:
        pp_repo.update({'PP_' + str(count) + '_' + child.tag: child.text})

    return pp_repo

#!/usr/bin/python3

'''
Compile and parse the results XML files into a pandas
DataFrame object.

@author: wraikes
'''

import os, xml.etree.ElementTree as eTree, pandas as pd

file_results = r'C:\Users\LENOVO\Desktop\Academic\horseracing\Data\xml\results'

def xml_transform_results(directory):
    os.chdir(directory)
    results_for_df = []

    for file in os.listdir():

        if file.endswith('.xml'):
            root = eTree.parse(file).getroot()
            results_for_df += root_data_results(root)

    df = pd.DataFrame(results_for_df)

    return df

def root_data_results(root):    
    root_data_repo = []

    for child in root:
        date = root.attrib['RACE_DATE'].replace('-', '')
        
        if child.tag == 'TRACK':
            track = child[0].text
 
        elif child.tag == 'RACE':
            race = child.attrib['NUMBER']
            race_results = race_data(child)

            for result in race_results:
                result_dict = {}
                result_dict.update({'race_date': date})                
                result_dict.update({'track': track, 'race': race})
                result_dict.update({'horse_name': result[0], 
                                    'result': result[1],
                                    'speed_rating': result[2]})
                root_data_repo.append(result_dict)
    
    return root_data_repo

def race_data(parent):
    race_data_repo = []
    
    for child in parent:         
        results = []
        
        if child.tag == 'ENTRY':
            for grandchild in child:
                
                if grandchild.tag == 'NAME':
                    results.append(grandchild.text.upper())
                    
                elif grandchild.tag == 'OFFICIAL_FIN':
                    results.append(grandchild.text)
                
                elif grandchild.tag == 'SPEED_RATING': 
                    results.append(grandchild.text)
                
        if results:
            race_data_repo.append(results)
                
    return race_data_repo

    


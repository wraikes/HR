import os, pandas as pd, numpy as np

#remove when ready
os.chdir('/home/wraikes/Programming/Personal_Projects/HorseRacing/Data/data_files')
hr_df = pd.read_csv("HR_DF.csv")


################################ Distance Conversion
distances = ['PP_{}_distance'.format(x) for x in range(1, 13)]
distances.insert(0, 'distance')

units = ['PP_{}_disttype'.format(x) for x in range(1, 13)]
units.insert(0, 'dist_unit')

dist_units = zip(distances, units)

for i in dist_units:
    hr_df[i[0]] = hr_df.apply(lambda x: x[i[0]] * 3 if x[i[1]] == 'Y' else x[i[0]], axis = 1)
    del hr_df[i[1]]


################################# Drop Columns
cols_to_drop = ['worktext', 'worknum', 'abbrevcond', 'aboutdist',
                'agerestric', 'claimprice', 'complined2',
                'complined3', 'complinedq', 'complineh2',
                'complineh3', 'complineho', 'country',
                'disttype', 'domesticpp', 'dqindicato',
                'foreignspe', 'jockdisp', 'jockfirst',
                'jocklast', 'jockmiddle', 'jocksuffix',
                'lineafter', 'linebefore', 'longcommen',
                'pulledofft', 'racedate', 'racegrade',
                'racetype', 'sealedtrac', 'sexrestric',
                'shortcomme', 'statebredr', 'trackcode',
                'trackname', 'vd_claim', 'vd_reason',
                'winddirect', 'windspeed', 'equipment',
                'racebreed', 'apprweight', 'surface',
                'courseid', 'trackcondi', 'J_SD_Last30_earnings', 
                'J_jock_disp', 'T_SD_Last30_earnings',
                'T_tran_disp', 'ae_flag', 'bet_opt', 
                'J_stat_breed', 'breeder', 'dam', 'dist_unit', 
                'dist_disp', 'owner_name', 'post_time', 'program', 
                'sire', 'equip', 'race_text', 'raceord', 
                'send_track', 'T_stat_breed', 'breed_type', 
                'wh_foaled', 'stkorclm', 'color']

for i in cols_to_drop:
    nums = hr_df.columns.str.contains(i)
    hr_df = hr_df.drop(hr_df.columns[nums], axis = 1)
    
################################### Create new features

hr_df['win'] = hr_df.where(hr_df['results'] == 1, 1, 0)

#morning odds
morning_odds = hr_df.morn_odds.str.split('/', expand = True)
hr_df['mo_1'] = morning_odds.iloc[:, 0].astype(int)
hr_df['mo_2'] = morning_odds.iloc[:, 1].astype(int)
hr_df = hr_df.drop('morn_odds', axis = 1)
hr_df['payout'] = hr_df['mo_1'] / hr_df['mo_2']
hr_df['odds'] = hr_df['mo_2'] / (hr_df['mo_2'] + hr_df['mo_1'])






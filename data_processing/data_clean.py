import os, pandas as pd, numpy as np, matplotlib.pyplot as plt
from sklearn.preprocessing import Imputer


#remove when ready
#os.chdir('/home/wraikes/Programming/Personal_Projects/HorseRacing/Data/data_files')
#hr_df = pd.read_csv("HR_DF.csv")
#hr_df = hr_df[hr_df['results'].notnull()]


################################ Distance Conversion


def dist_change(df):
    distances = ['PP_{}_distance'.format(x) for x in range(1, 13)]
    distances.insert(0, 'distance')

    units = ['PP_{}_disttype'.format(x) for x in range(1, 13)]
    units.insert(0, 'dist_unit')

    dist_units = zip(distances, units)

    for i in dist_units:
        df[i[0]] = df.apply(lambda x: x[i[0]] * 3 if x[i[1]] == 'Y' else x[i[0]], axis = 1)
        del df[i[1]]

    return df
    
################################# Drop Columns
def col_drop(df):

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
        nums =df.columns.str.contains(i)
        df.drop(df.columns[nums], axis = 1, inplace = True)
    
    return df
    
################################### Create new features

def new_features(df):
    df['win'] = np.where(df['results'] == 1, 1, 0)

    #morning odds
    df = df[df.morn_odds.str.contains('/')]
    morning_odds = df.morn_odds.str.split('/', expand = True)
    df['mo_1'] = morning_odds.iloc[:, 0].astype(int)
    df['mo_2'] = morning_odds.iloc[:, 1].astype(int)
    df['payout'] = df['mo_1'] / df['mo_2']

    df['odds'] = df['mo_2'] / (df['mo_2'] + df['mo_1'])
    df['odds'] = df['odds'] / df.groupby(['race_date', 'track', 'race']).odds.transform('sum')
    df.drop(['morn_odds', 'mo_1', 'mo_2'], axis = 1, inplace = True)

    #Recode "Others"
    courses = ['D', 'E', 'T']
    df['course_id'] = np.where(df['course_id'].isin(courses), 
                               df['course_id'], 'Other')

    sex = ['C', 'F', 'G', 'M']
    df['sex'] = np.where(df['sex'].isin(sex), df['sex'], 'Other')

    pp_1_raceclass = ['CL', 'MC', "MS", 'AL', 'OC', 'ST', 'SA', 'SO']
    df['PP_1_raceclass'] = np.where(df['PP_1_raceclass'].isin(pp_1_raceclass), 
                                    df['PP_1_raceclass'], 'Other')

    #Create CV column
    df['cv'] = df.groupby(['race_date', 'track', 'race']).grouper.group_info[0]

    #Remove horse_name and track, unneeded columns for analysis.
    df.drop(['horse_name', 'track'], axis = 1, inplace = True)
    
    return df
    
################################### Remove features with many NaNs

#Explore trade-offs of cutoff values
#cutoff = np.linspace(0, .2, 200)
#df_shapes = []
#
#for i in cutoff:
#    df_shapes.append(sum(1 - hr_df.count() / hr_df.shape[0] < i))
#
#df_shapes = pd.Series(df_shapes)
#df_shapes.index = cutoff
#
#plt.plot(df_shapes)

#Chose 0.15 with thought of filling in NaNs

def remove_na(df, cutoff = 0.15):
    '''Removes rows with NaN as 'result'. Also removes columns that meet less
    than the cutoff rate.
    '''
    df = df[df['results'].notnull()]
    
    new_index = 1 - (df.count() / df.shape[0]) < cutoff
    df = df.iloc[:, new_index.values]
    return df
                                        
                                        
def imputer(df, method = 'mean'):
    imputer = Imputer(strategy = method)

    for col in df.columns:
        if df[col].dtype == 'float64':
            df[col] = imputer.fit_transform(df[col].reshape(-1, 1))

def create_dummies(df):
    cols_object = [x for x in df.columns if df[x].dtype == 'O']
    return pd.get_dummies(df, dummy_na = True, columns=cols_object)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

def data_clean(df):
    
    new_df = dist_change(df)
    new_df = col_drop(df)
    new_df = new_features(df)
    new_df = remove_na(df)
    new_df = imputer(df)
    new_df = create_dummies(df)
    
    return new_df

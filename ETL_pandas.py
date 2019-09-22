# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 15:35:42 2019

@author: Sumon
"""
#import all the necessary libraries
import io
import pandas as pd
import requests as r

# all the file places into varaibles
url = ' http://drd.ba.ttu.edu/isqs6339/hw/hw2/'
file_1 = 'players.csv'
file_2 = 'player_sessions.csv'
path = 'C:\TTU_Masters\BusinessIntelligence\Quiz2/'
file_out1 = 'dam_heal_sess_clan_.csv'
file_out2 = 'dam_heal_pos_.csv'
file_out3 = 'merg_output_.csv'

#pull players
res = r.get(url + file_1)
res.status_code
df_player = pd.read_csv(io.StringIO(res.text),delimiter='|') 
df_player

#see 1st few rows of data for both player dataset
df_player.head()

#pull player sessions
res = r.get(url + file_2)
res.status_code
df_pl_ses = pd.read_csv(io.StringIO(res.text))
df_pl_ses

#see 1st few rows of data for both player sesion dataset
df_pl_ses.head()
df_player_merge_id = df_player.merge(df_pl_ses, how='inner', on=['playerid'])
df_player_merge_id.head()
df_player_merge_id.count()

#Types look good
df_player_merge_id.dtypes

#writing it to excel to check all the values to get better idea about the missing values
#df_player_merge_id.to_csv(path + file_out, index=False)

#checking the NA values
df_player_merge_id[df_player_merge_id['clan'].isnull()]
df_player_merge_id[df_player_merge_id['damage_done'].isnull()]

#filling the missing values of 'clan' column with 'LOD'. as all the missing value of 'clan'are with 'handle' name starting with 'v', i am putting the values all together
df_player_merge_id['clan'].fillna('LoD', inplace=True)

#filling the missing values of 'damange_done', taking the mean of existing'damange_done' values corresponds with the 'playerid'
m1 = (df_player_merge_id['playerid'] == 1)
m2 = (df_player_merge_id['playerid'] == 2)
m3 = (df_player_merge_id['playerid'] == 3)
m6 = (df_player_merge_id['playerid'] == 6)
m10 = (df_player_merge_id['playerid'] == 10)
m12 = (df_player_merge_id['playerid'] == 12)
m13 = (df_player_merge_id['playerid'] == 13)

df_player_merge_id.loc[m1,'damage_done'] = df_player_merge_id.loc[m1,'damage_done'].fillna(int(df_player_merge_id.loc[m1,'damage_done'].mean()))
df_player_merge_id.loc[m2,'damage_done'] = df_player_merge_id.loc[m2,'damage_done'].fillna(int(df_player_merge_id.loc[m2,'damage_done'].mean()))
df_player_merge_id.loc[m3,'damage_done'] = df_player_merge_id.loc[m3,'damage_done'].fillna(int(df_player_merge_id.loc[m3,'damage_done'].mean()))
df_player_merge_id.loc[m6,'damage_done'] = df_player_merge_id.loc[m6,'damage_done'].fillna(int(df_player_merge_id.loc[m6,'damage_done'].mean()))
df_player_merge_id.loc[m10,'damage_done'] = df_player_merge_id.loc[m10,'damage_done'].fillna(int(df_player_merge_id.loc[m10,'damage_done'].mean()))
df_player_merge_id.loc[m12,'damage_done'] = df_player_merge_id.loc[m12,'damage_done'].fillna(int(df_player_merge_id.loc[m12,'damage_done'].mean()))
df_player_merge_id.loc[m13,'damage_done'] = df_player_merge_id.loc[m13,'damage_done'].fillna(int(df_player_merge_id.loc[m13,'damage_done'].mean()))
df_player_merge_id.count()

#df_player_merge_id.to_csv(path + file_out, index=False) to check manually

#Now, as all missing values are filled, lets do other calculations
#add a column name 'player_performance_metric' with given calculation
df_player_merge_id['player_performance_metric'] = (df_player_merge_id['damage_done']*3.125 + df_player_merge_id['healing_done']*4.815)/4
df_player_merge_id.count()

#add another column 'dps_quality' with given conditions
df_player_merge_id['dps_quality'] = 'Low'
df_player_merge_id['dps_quality'][df_player_merge_id['damage_done'] > 600000] = 'High'
df_player_merge_id['dps_quality'][(df_player_merge_id['damage_done'] >= 400000) & (df_player_merge_id['damage_done']<600000)] = 'Medium'
df_player_merge_id['dps_quality'][df_player_merge_id['damage_done'] < 400000] = 'Low'
df_player_merge_id.count()
df_player_merge_id.head()

#df_player_merge_id.to_csv(path + file_out, index=False) to check manually

#add another column 'player_dkp_gen_rate' according to given calculation and condition
df_player_merge_id['player_dkp_gen_rate'] = 100
df_player_merge_id.loc[df_player_merge_id.dps_quality == 'High', 'player_dkp_gen_rate'] = df_player_merge_id['player_performance_metric']*1.25
df_player_merge_id.loc[df_player_merge_id.dps_quality == 'Medium', 'player_dkp_gen_rate'] = df_player_merge_id['player_performance_metric']*1.15
df_player_merge_id.loc[(df_player_merge_id.dps_quality == 'Low') & (df_player_merge_id.clan != 'LoD'), 'player_dkp_gen_rate'] = df_player_merge_id['player_performance_metric']*.85
df_player_merge_id.loc[(df_player_merge_id.dps_quality == 'Low') & (df_player_merge_id.clan == 'LoD'), 'player_dkp_gen_rate'] = df_player_merge_id['player_performance_metric']*2.35
#df_player_merge_id.to_csv(path + file_out, index=False) to check manually

df_player_merge_id['player_dkp_gen_rate'].dtype
df_player_merge_id.dtypes
#df_player_merge_id['player_dkp_gen_rate']= pd.to_numeric(df_player_merge_id['player_dkp_gen_rate'])
#df_player_merge_id.iloc[24,:]

#writing CSV
csv1= df_player_merge_id.groupby(by=['session','clan'])[['damage_done','healing_done']].mean()
csv1.to_csv(path + file_out1, index=False)
csv2=df_player_merge_id.groupby(by='position')[['damage_done','healing_done']].mean()
csv2.to_csv(path + file_out2, index=False)
csv3=df_player_merge_id.sort_values(by='player_dkp_gen_rate')
csv3.to_csv(path + file_out3, index=False)

#Question Answers 1
# The quality of the data was ok. There were some missing values for 'clan' and 'damage_done' column
# First and second file's delimeter was different. In order to merge it, had to 
#change the 'players.csv' to comma delimeter.


#Answer2
# for filling the missing values of 'clan' column I put the value 'LoD' whose 'handle' name was 
#starting with 'v'. It was easy as all the 'handle' name who has missing 'clan', was starting with 'v'.
#If it was different then had to do using split function taking the 1st string of the 'handle' name 
#and put the value of 'clan' according to it.
#for the missing value of 'damage_done' column, i checked manually for which 'playerid' it was missing. 
#Then for the missing ones took the mean of the existing values and fill the missing 'damage_done' values. 
#I could have use the mode (appaears most)and median(center value).As i thought, average or mean will give 
#the most accurate value, as it takes the average performance damage done for each player and fill 
#the missing values with it.


# Answer 3
#i manually checked the 'damage_done' values according to 'playerid'. 
#As there was not a lots of data, i could check it manually by writting the file to a csv. 
#If it had more data, i had to check the NA values with code according to 'playerid'. 
#This is also same for the 'clan' missing values. 
#I could have check it with command, if it had differnt 'handle'name. 
#For filling the 'damage_done' values, I filled with mean depending with the 'playerid'. 
#It could be done with mode and mediun also.


#Answer 4
#maximun damage_done for a player id
df_player_merge_id.loc[df_player_merge_id['damage_done'].idxmax()]
#whose playerid  is 10 from OOTM clan
#output of the previuos line of code, showing the desired result
#playerid                             10
#handle                       mindmelter
#clan                               OOTM
#best_genre                          pve
#position                            dps
#session                              17
#damage_done                      998047
#healing_done                      65694
#player_performance_metric        858803
#dps_quality                        High
#player_dkp_gen_rate          1.0735e+06
#Name: 362, dtype: object

#maximun healing_done for a player id
df_player_merge_id.loc[df_player_merge_id['healing_done'].idxmax()]
#whose playerid  is 4 from TL clan
#output of the previuos line of code, showing the desired result
#playerid                               4
#handle                             bakko
#clan                                  TL
#best_genre                            rp
#position                          healer
#session                               10
#damage_done                         9739
#healing_done                      995159
#player_performance_metric    1.20553e+06
#dps_quality                          Low
#player_dkp_gen_rate           1.0247e+06
#Name: 127, dtype: object

#maximun player_performance_metric for a player id
df_player_merge_id.loc[df_player_merge_id['player_performance_metric'].idxmax()]
#whose playerid  is 4 from bakko clan
#output of the previuos line of code, showing the desired result
#playerid                               4
#handle                             bakko
#clan                                  TL
#best_genre                            rp
#position                          healer
#session                               10
#damage_done                         9739
#healing_done                      995159
#player_performance_metric    1.20553e+06
#dps_quality                          Low
#player_dkp_gen_rate           1.0247e+06

#maximun player_dkp_gen_rate for a player id
df_player_merge_id.loc[df_player_merge_id['player_dkp_gen_rate'].idxmax()]
#whose playerid  is 3 from TL clan
#playerid                               3
#handle                           molbrew
#clan                                  TL
#best_genre                           pvp
#position                             dps
#session                               32
#damage_done                       982598
#healing_done                       98084
#player_performance_metric         885723
#dps_quality                         High
#player_dkp_gen_rate          1.10715e+06
#Name: 107, dtype: object
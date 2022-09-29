# -*- coding: utf-8 -*-
"""
EDGE PULL 12 SEPT 2016
Created on Thu Jul 28 13:39:03 2016

@author: sheble

find where NOMA values come in

Answer: original encounter data, there are 400 'NOMATC' entries

get dataset without noma entries
plus rerun all demo
get MIN & Max date entries for each diagnosis by patient
save data with and without isolate data to run expected values
and new observed edges

"""

import pandas as pd
import numpy as np
import os



# ICD-9 Diagnosis
data_icd9diag = pd.read_csv("data/dr1400_output_icd9_diagnosis.csv", header=0, sep="|", usecols=['PATIENT_KEY', 'ENCOUNTER_KEY', 'DIAGNOSIS_DATE', 'DIAGNOSIS_CODE']) #, nrows=1000

diag_orig_len = len(data_icd9diag)

data_icd9diag = data_icd9diag.dropna()

diag_orig_minus_na = len(data_icd9diag)


df_noma = data_icd9diag[data_icd9diag['DIAGNOSIS_CODE'].str.contains('NOMA')]

#orig_len_enc = len(data_icd9diag)

#data_icd9diag = data_icd9diag.dropna()

#orig_minus_dropna = len(data_icd9diag)

#df_noma = data_icd9diag[data_icd9diag['DIAGNOSIS_CODE'].str.contains('NOMA')]

df_noma.head(5)

number_null_encounter_values = diag_orig_len - diag_orig_minus_na

# get dataset without noma entries
data_icd9diag = data_icd9diag[~data_icd9diag['DIAGNOSIS_CODE'].str.contains('NOMATC')]

# length after dropping NOMATC strings
orig_minus_na_and_nomatc = len(data_icd9diag)

# count of dropped nomatc AND na items:
number_na_and_nomatc_dropped = diag_orig_len - orig_minus_na_and_nomatc

# strip out extra spaces, take '.##' out of icd-9 codes in our emr records
data_icd9diag['DIAGNOSIS_CODE'] = data_icd9diag['DIAGNOSIS_CODE'].str.strip().str.replace('\.\d{0,2}','')

# length before diag dupes dropped
diag_b4_dupe_drop = len(data_icd9diag) # same as 'number_na_and_nomatc_dropped'

# drop cases where same diagnosis was given to same patient on same data/encounter
# dupes typically because diff kinds of diag entered (e.g., 'at discharge')
# technically, using the min & max should obviate the need for this
data_icd9diag = data_icd9diag.drop_duplicates() # uses all columns by default

# length after diag dupes dropped
diag_after_dupe_drop = len(data_icd9diag)

data_icd9diag.head()

# don't need encounter key
data_icd9diag.drop('ENCOUNTER_KEY', axis=1, inplace=True)
# grouped = data_icd9diag.groupby(['PATIENT_KEY', 'ENCOUNTER_KEY']).count()

# rename columns... shorter, friendlier to type
data_icd9diag.columns=['patient', 'date', 'diag']

# keep only the first & last entries for each diagnosis type
df = data_icd9diag.groupby(['patient', 'diag'], as_index=False).agg({'date' : [min, max]})
stacked = df.set_index(['patient', 'diag']).stack()
stacked.head()
df2 = stacked.reset_index()
df2.head()
df2.drop('level_2', axis=1, inplace=True)
df2 = df2.drop_duplicates()

# ADD the DEMO data
# data_demo = pd.read_csv("EMR/fiveYear/csv/demographics.csv", header=0, sep=',') #, nrows=5000
data_demo = pd.read_csv("data/dr1400_output_demographics.csv", header=0, sep='|')


data_demo['BIRTH_DATE'] = pd.to_datetime(data_demo['BIRTH_DATE'], format = '%Y-%m-%d') # format='%d%b%Y:%H:%M:%S')

# get the birth year from BIRTH_DATE
data_demo['birth_year'] = data_demo['BIRTH_DATE'].map(lambda x: x.year)

# to get ages, first get enddate... dataset ends in 2011
data_date = ('2011-12-31')
# data_date = ('2011')
data_demo['data_date']=pd.to_datetime(data_date, format = '%Y-%m-%d')

data_demo['data_year']=data_demo['data_date'].map(lambda x: x.year)

data_demo['age'] = data_demo['data_year'] - data_demo['birth_year']

data_demo.head()

# Hispanic or Latino ethnicity prioritized over race entries
data_demo['race_ethn']=np.where(data_demo['ETHNICITY']=='HISPANIC OR LATINO', 'HISPANIC OR LATINO', data_demo['RACE'])

# drop unneeded demo data 
data_demo = data_demo[['PATIENT_KEY', 'GENDER', 'race_ethn', 'age']]

# drop very very old people; drop genders other than male, female, drop ethnicities/races we are not using:
# drop if age <0 or > 115
data_demo=data_demo[data_demo.age >= 0]
data_demo=data_demo[data_demo.age <= 115]

# drop ambiguous/missing gender data
gender_keep = ['FEMALE', 'MALE']
data_demo = data_demo[data_demo['GENDER'].isin(gender_keep)]

# keep only race/ethn categories for which we have a good bit of data
race_ethn_keep = ['ASIAN','BLACK','HISPANIC OR LATINO','WHITE']
data_demo = data_demo[data_demo['race_ethn'].isin(race_ethn_keep)]

# get rid of spaces in 'hispanic or latino'... esp since using this for file names later
df['race_ethn'] = df['race_ethn'].str.replace(' ', '-')

count_patients_after_race_ethn_drop = len(data_demo)

# rename columns... friendlier format, less verbose pd.merge statement (demo & diag now have 'patient' columns)
data_demo.columns = ['patient', 'gender', 'race_ethn', 'age']

number_pat_diag_date_b4_merge = len(df2)
number_pat_demo_b4_merge = len(data_demo)

# inner join: only where we have patient keys for both data_demo and df2
df = pd.merge(data_demo, df2, on='patient', how='inner')

# prep age bins & their labels/entries
bins = [0, 1, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
group_labels = ['0-to-12mo', '1-to-2', '3-to-4', '5-to-9', '10-to-14', '15-to-19', '20-to-24', '25-to-29', '30-to-34', '35-to-39', '40-to-44', '45-to-49', '50-to-54', '55-to-59', '60-to-64', '65-to-69', '70-to-74', '75-to-79', '80-to-84', '85-to-89', '90-and-up']

# bin data
age_group = pd.cut(df['age'], bins, right=False, labels=group_labels, retbins=True, precision=2, include_lowest=True)
df['age_group'] = pd.cut(df['age'], bins, right=False, labels=group_labels, retbins=False, precision=2, include_lowest=True)


df.head()

# drop age column... don't need this
df.drop('age', axis=1, inplace=True)

# make director, prepare to save files for each group... with isolates
os.mkdir('data/pat_diag_groups_minmax_w_isolates')
dir_name = 'data/pat_diag_groups_minmax_w_isolates/'

df_w_isolates_gr = df.groupby(['gender', 'race_ethn', 'age_group'])

for name, group in df_w_isolates_gr:
    file_name = str(name[0]) + '_' + str(name[1]) + '_' + str(name[2])
    print(file_name)
    save_path = os.path.join(dir_name, file_name + '.csv')   
    group.to_csv(str(save_path), header=True, index=False)

# also save file with all groups, including isolates
# in case one file easier to work with
os.mkdir('data/pat_diag_minmax_single_files')

df.to_csv('data/pat_diag_minmax_single_files/all_groups_w_isolates.csv', header=True, index=False)

# Second, get items without isolates

'''
# could id isolates:
isolates = df.groupby(['patient']).filter(lambda group: len(group) == 1)
number_isolate_diag = len(isolates['PATIENT_KEY'].unique())
# get list of patients with only 1 diagnosis, drop
'''

#or, could id patients w/ >1 diag:

df_mult_diag = df.groupby(['patient'], as_index=False).filter(lambda group: len(group) > 1)

# single file with all groups, no isolates
df_mult_diag.to_csv('data/pat_diag_minmax_single_files/all_groups_no_isolates.csv', header=True, index=False)

# make directory, prepare to save files for each group... no isolates included
os.mkdir('data/pat_diag_groups_minmax_no_isolates')
dir_name = 'data/pat_diag_groups_minmax_no_isolates/'

df_mult_diag_gr = df.groupby(['gender', 'race_ethn', 'age_group'])

for name, group in df_mult_diag_gr:
    file_name = str(name[0]) + '_' + str(name[1]) + '_' + str(name[2])
    print(file_name)
    save_path = os.path.join(dir_name, file_name + '.csv')   
    group.to_csv(str(save_path), header=True, index=False)


# End
#######



#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:51:15 2016

@author: ShebleAdmin
building on one of Rick's earlier scripts
"""

# import sys
import simplejson as json
import pandas as pd

rec=[]
record={}
rec_list=[]
key=""
concat=False
records_list = []

#fileName=sys.argv[1]
wos_plaintext = 'CogNeuroSci_raw_clean.txt'
fp = '/Users/ShebleAdmin/CogNeuroSci/'
wos_tsv = 'CogNeuroSci_raw_clean.csv'

wosin = fp + wos_plaintext
tsvout = fp + wos_tsv

# Read the input file
#with open(sys.argv[1]) as f:
with open (wosin, 'r') as f:
    with open(tsvout, 'w+') as of:
        for line in f:
            line = line.replace('\ufeff','')
    #        print line    
            if len(line.strip()) == 0:
                continue  
            rec = line.rstrip().split(" ", 1)
            # get rid of empty rec list
            if len(rec) > 1:
            # set key == tag or ''            
                value=rec[1].strip()
            # print(value)
            # print(rec)
            # test: end of record?              
            if key == "ER":
            # record["fileName"]=fileName
                record["fileName"]=wos_plaintext
            # print("Record: ")
              # append record to list of records before resetting, getting the next record
                records_list.append(record)              
                print(json.dumps(record,sort_keys=False, indent=4 * ' '))
                record={}
            # concatenate items that go across lines, make use of the split on spaces,
            if rec[0] == '' and concat == False:
                concat=True
                rec_list=[]
                rec_list.append(record[key])
                rec_list.append(value)
                record[key]=rec_list
            elif rec[0] == '':
                record[key].append(value)
            else:
                concat=False
                key=rec[0]
                record[key]=value

semicolon_keys = ['AU', 'AF', 'CR']
no_semis_keys = ['AB', 'C1', 'DE','ID','EM','FU','FX','OI', 'RP', 'TI']

for recdict in records_list:
     for key, value in recdict.items():
         if key in semicolon_keys and type(value) == list:
             recdict[key] = '; '.join(value)
         elif key in no_semis_keys and type(value) == list:
             recdict[key] = ' '.join(value)

df = pd.DataFrame(records_list)

df.drop(['FN', 'VR'], inplace=True, axis=1)
df.to_csv(tsvout, index=False, sep='\t', encoding='utf-8')

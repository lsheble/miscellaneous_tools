#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 17:06:58 2016
@author: ShebleAdmin

MeSH Descriptor file, 2017 prelim version from:
ftp://nlmpubs.nlm.nih.gov/online/mesh/MESH_FILES/asciimesh/d2017.bin
used in initial version
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
mesh_plaintext = 'mesh_ascii_d2017.txt'
fp = '/Users/ShebleAdmin/'
mesh_tsv = 'mesh_ascii_d2017.csv'

meshin = fp + mesh_plaintext
tsvout = fp + mesh_tsv

# Read the input file
#with open(sys.argv[1]) as f:
with open (meshin, 'r') as f:
#    with open(tsvout, 'w+') as of:
    i = 0
    for line in f:    
        if line == "*NEWRECORD":
            record={}
        rec = line.rstrip().split("=", 1)
        if len(rec) > 1:
            record[rec[0].strip()]=rec[1].strip()
        if len(line.strip()) == 0:
            records_list.append(record) 
    print(len(records_list))

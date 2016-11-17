#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 17:06:58 2016

@author: ShebleAdmin

python >= 3.2
(b/c 'next' with csv module)
"""

import csv
# import sys

file_ = ''
out_file = ''
# file_ = sys.argv[1]
# out_file = sys.argv[2]

with open(file_,'r') as csvfile:
    text_ = 'FN Thomson Reuters Web of Science™\nVR 1.0\n'
    csv_reader = csv.reader(csvfile,delimiter='\t')
    headers = next(csv_reader)
    # strip BOM
    headers[0] = headers[0].replace('\ufeff', '')
#    print(headers)
    for row in csv_reader:
        i = 0
        for column in row:
            if column is None or column == '':
                i += 1
    for row in csv_reader:
        i = 0
        for column in row:
            if column is None or column == "":
                i += 1
            elif headers[i] == 'C1':
                text_ += headers[i] + ' ' + str(column).replace('; [', '\n   [') + '\n'
                i += 1
            elif headers[i] == 'AU|AF|ID|DE|WC|EM|OI|RI|FU|CR':
                text_ += headers[i] + ' ' + str(column).replace('; ','\n   ') + '\n'
                i += 1
            else:
                text_ += headers[i] + ' ' + str(column).replace('; ','\n   ') + '\n'
                i += 1
        text_ += 'ER\n\n'
    text_ += 'EF'
#    print(text_)
with open(out_file,'w') as output:
    output.write(text_)

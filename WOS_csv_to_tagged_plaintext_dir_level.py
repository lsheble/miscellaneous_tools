#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 09:44:59 2016

@author: ShebleAdmin

convert all the files in a directory: WOS csv to tagged plain text
should check more to see if there are other fields that need to be handled in special ways

"""

import csv
import os
#import sys


# dir_name = sys.argv[1]
# out_subfolder_name = sys.argv[2] # name of subdirectory for outfiles (e.g., 'af_files_plaintext'), hard coded here, dir structure not great

dir_name = '<path_to_in_files_w_in_subfolder>'


def csv_to_plain(file):
    out_file = str(file.replace('.csv', '_converted.txt'))
    out_file = str(out_file.replace('af_files', 'af_files_plaintext'))
    with open(file,'r') as csvfile:
        text_ = 'FN Thomson Reuters Web of Science™\nVR 1.0\n'
        csv_reader = csv.reader(csvfile,delimiter='\t')
        headers = next(csv_reader)
        # strip BOM
        headers[0] = headers[0].replace('\ufeff', '')
        print(headers)
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
        print(text_)
    print(out_file)
    with open(out_file,'w') as output:
        output.write(text_)


for infile in os.listdir(dir_name):
    read_infile = os.path.join(dir_name, infile)
    print(read_infile)
    csv_to_plain(read_infile)

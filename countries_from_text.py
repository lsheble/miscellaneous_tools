# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 06:40:46 2017
@author: ShebleAdmin
"""

import pandas as pd


fp = <fp>
# list of countries to find
country_list = 'country_list_US_dept_of_state.txt'
countries_in = fp + country_list


# text file with just C1 field
textin = 'C1s_to_tag.txt'# 
readtexts = fp + textin


# Read in text file that has the list of countries in it that we want to match
with open(countries_in, 'r') as countries:
    country_list = countries.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
country_list = [x.strip() for x in country_list] 
# get rid of first item in the list... the note on where the list came from
country_list.pop(0)


df = pd.read_csv(readtexts, sep='\t')
df.head()


def extract_places(cell_text):
    places_only = ''
    for i in country_list:
        if i in cell_text:
            places_only += i + ', '
    places_only = places_only.rstrip(', ')
    return places_only


df['countries']=df['C1'].apply(extract_places)

dfc = df['countries'].str.get_dummies(sep=", ")

c_cts = pd.DataFrame(dfc.sum(axis=0))
c_cts.index = c_cts.index.str.lower()
c_cts.head()
c_cts.index.set_value(c_cts.index, 'usa', 'united states')
c_cts.reset_index(inplace=True)
c_cts.columns=['region', 'value']

country_tally = 'country_occurrences_by_paper.tsv'
country_tally_out = fp + country_tally
c_cts.to_csv(country_tally_out, sep='\t', header=True, index=False)

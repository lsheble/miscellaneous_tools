# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 07:21:33 2016

@author: ShebleAdmin

query crossref with a list of cites that are just dumped into query with minimal parsing
should do this as a session with Requests, I think

used to deal with a file with references that were all in a jumble wrt format, etc
scores from crossref seem to work pretty well as estimate of likelihood of match,
even with data that is somewhat rough

"""


import re
import requests
import json
import pandas as pd
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

#### Set fp variable to your folder with file to be processed ####
fp = "/<path_to_file_with_jumble of references>/" 
examples = fp + "publist_stacked_nonMacWin_zapGrem_reduced.csv"




def build_query_url(citation):
    query_url = "http://api.crossref.org/works?query="
#    citation = re.sub('[&,.()\[\]:/"+Õ\_@Ò\*\n]', '', citation)
    citation = re.sub('[^\s\da-zA-Z-/]', ' ', citation)
    citation = re.sub(r'\s\D{1,2}\s{0,1}\D{0,1}\s', ' ', citation)
    citation = re.sub(r'\s{2,10}', ' ', citation)
    citation = re.sub(r'\d-\d', ' ', citation)
    citation.strip(' ')
    citation = re.sub(r'\s', '+', citation)    
    query_url = query_url + '"' + citation + '"' + '&rows=1' # &rows=1 limits to the first result (&rows=0 to get a summary of search results)
    return query_url

 
# THIS ONE WORKS BEST AT THE MOMENT think about doing something else with the affiliation data (but there was essentially none for my set) & get rid of 'str' in code
def construct_author(author_item):
    count = 0
    author_construct = ''
    for item in author_item:
        if count < (len(author_item)-1):
            if 'given' in item:
                author_construct = author_construct + str(item['family']) + ', ' + str(item['given']) + ' (' + str(item['affiliation']) + '); '
                count += 1
            else:
                author_construct = author_construct + str(item['family']) + ' (' + str(item['affiliation']) + '); '
                count += 1
        else:
            if 'given' in item:
                author_construct = author_construct + str(item['family']) + ', ' + str(item['given']) + ' (' + str(item['affiliation']) + ')'
                count += 1
            else:
                author_construct = author_construct + str(item['family']) + ' (' + str(item['affiliation']) + ')'
                count += 1
    return author_construct
    
    
def construct_title(title_item):
    count=0
    title_construct = ''
    for item in title_item:
        if count < (len(title_item)-1):
            title_construct = title_construct + item + '; '
            count += 1
        else:
            title_construct = title_construct + item
            count += 1
    return title_construct
            

def construct_subject(subject_item):
    count=0
    subject_construct = ''
    for item in subject_item:
        if count < (len(subject_item)-1):
            subject_construct = subject_construct + item + '; '
            count += 1
        else:
            subject_construct = subject_construct + item
            count += 1
    return subject_construct

    

def extract_json_fields(data):
    reference = []
    doi = data['message']['items'][0]['DOI']
    year = str(data['message']['items'][0]['issued']['date-parts'][0][0])
    subject = "data['message']['items'][0]['subject']"
    if 'subject' in data['message']['items'][0]:
        subject = construct_subject(data['message']['items'][0]['subject'])
    else: 
        subject = u'NA'
    if 'author' in data['message']['items'][0]:
        author = construct_author(data['message']['items'][0]['author'])
    else:
        author = 'NA'
    if 'score' in data['message']['items'][0]:    
        score = data['message']['items'][0]['score']
    else:
        score = 'NA'
    if 'volume' in data['message']['items'][0]:
        volume = data['message']['items'][0]['volume']
    else:
        volume = u'NA'
    if 'issue' in data['message']['items'][0]:
        issue = data['message']['items'][0]['issue']
    else:
        issue = u'NA'
    title = data['message']['items'][0]['title'][0]
    if 'alternative-id' in data['message']['items'][0]:
        alternative_id = data['message']['items'][0]['alternative-id'][0]
    else:
        alternative_id = u'NA'
    container_title = construct_title(data['message']['items'][0]['container-title'])
    if 'page' in data['message']['items'][0]:
        page = data['message']['items'][0]['page']
    else:
        page = u'NA'
    reference.extend([subject, author, year, title, container_title, volume, issue, page, doi, alternative_id, score])
    return reference



df = pd.read_table(examples, sep=',', header=0, verbose=True, quotechar='"',  error_bad_lines=True, warn_bad_lines=True)
citations = df['citestring'].tolist()
rows = []
errors = []
for item in citations:
    query_item = build_query_url(item)
    request = requests.get(query_item)
#    print(request.text)
    try:    
        refs = request.text
    except:
        errors.append('no text from crossref')
        print(errors)
#    print(refs)
    data = json.loads(refs)
    data_extract = extract_json_fields(data)
    rows.append(data_extract)
    
df_refs = pd.DataFrame(rows)
df_refs.columns = ['subject', 'author', 'year', 'title', 'journal', 'volume', 'issue', 'page', 'doi', 'alternative_id', 'score']

df_refs.head()
df_out = pd.concat([df, df_refs], axis=1)
df_out[['citestring', 'author', 'title']].head()
df_out.to_csv('final/df_out_all_items_from_crossref_v3.csv', sep='\t', header=True)

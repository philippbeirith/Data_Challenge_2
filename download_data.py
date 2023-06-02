#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 16:38:12 2023

@author: philippbeirith
"""
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import zipfile
import sqlite3
import sqlalchemy
from tqdm import tqdm

#first create the data base
from initialize_db import create_db
create_db()

#Open the database connection for use later
conn = sqlite3.connect('crime_data') 

#Get the links for the latest datasets
url = "https://data.police.uk/data/archive/"
response = requests.get(url)

download_list = []

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    for link in links:
        if link[-3:] == 'zip' and str(link) not in ['/data/archive/latest.zip','/data/neighbourhood.zip']:
            download_list.append(link)
failed_extensions = []

   
for extension in tqdm(download_list):
    try:
            
        print('next link')
        url = str('https://data.police.uk'+extension)
        print(url)
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        response = session.get(url)
        
        with open("response.zip", "wb") as f:
            f.write(response.content)
        
        with zipfile.ZipFile('response.zip', 'r') as zipobj:
            full_list = zipobj.namelist()
            street_list  = []
            for item in full_list:
                if str(item[-10:]) == 'street.csv':
                    street_list.append(item)
            
            neighbourhood_list= []
            for neighbourhood in street_list:
                if neighbourhood.split('-')[3] in ['hertfordshire','metropolitan']:
                    neighbourhood_list.append(neighbourhood)
            
            for csv in tqdm(neighbourhood_list):
                df = pd.read_csv(zipobj.open(csv), sep=',')
                df.astype(str)
                df = df.dropna(subset=['LSOA name', 'Crime type'])
                df = df[df['LSOA name'].str.contains('Barnet')]
                #df = df[df['Crime type'].str.contains('Burglary')]
                df.to_sql('temp',conn, if_exists = 'replace')
                conn.execute('''
                             insert or ignore into street select * from temp
                             ''')
    except:
        failed_extensions.append(extension)

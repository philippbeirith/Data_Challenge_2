#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:56:16 2023

@author: philippbeirith
"""
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/crime_data')
c = conn.cursor()

def get(sql):
    return(pd.read_sql(sql, conn))

def sql_to_csv(query, filepath:str):
    get(query).to_csv(str(filepath))

#This will download a csv of columns: {month, LSOA code, Crime type} to be used for the heatmaps.
geographical_mappings_cloropreth = 'select month, "LSOA code", "Crime type" from street where month > "2022-01-01"'
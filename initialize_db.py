#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 12:53:15 2023

@author: philippbeirith
"""
import sqlite3

def create_db():
    conn = sqlite3.connect('data/crime_data')
    c = conn.cursor()
    
    c.execute('''
              CREATE TABLE IF NOT EXISTS street
              ([Index] INT,
               [Crime ID] TEXT, 
               [Month] TEXT, 
               [Reported by] TEXT,
               [Falls within] TEXT,
               [Longitude] REAL, 
               [Latitude] REAL, 
               [Location] TEXT, 
               [LSOA code] TEXT,
               [LSOA name] TEXT, 
               [Crime type] TEXT, 
               [Last outcome category] TEXT,
               [Context] TEXT)
              ''')
    
    conn.commit()

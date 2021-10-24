# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 13:56:10 2021

@author: Shreyes
"""
from bs4 import BeautifulSoup
import csv
import requests
import os
import pandas as pd

excel = "https://docs.google.com/spreadsheets/d/1c97BUzu3nbIA_T4iZdu0a6nTBdWj5P8ZTg1q_lnYubs/edit#gid=0"

def scrapeAndGenerateCsv():
    sheetHtml = requests.get(excel)
    soup = BeautifulSoup(sheetHtml.text, "lxml")
    tables = soup.find_all("table")
    index = 0
    for table in tables:
        with open(str(index) + ".csv", "w", encoding = 'utf8') as f:
            wr = csv.writer(f, lineterminator = '\n' ,quoting=csv.QUOTE_NONNUMERIC)
            wr.writerows([[td.text for td in row.find_all("td")] for row in table.find_all("tr")])
        index = index + 1
        

def cleanDataFrame():
    if not os.path.isfile('0.csv'):
        scrapeAndGenerateCsv()
    df = pd.read_csv('0.csv', skiprows = [0])
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(axis = 0, how = 'all')
    return df[df.columns[[0,3,4,5,6]]]

def buildUrl():
    df = cleanDataFrame()
    urls = []
    '''https://raw.githubusercontent.com/ShreyesBhat/smart_and_health_buildings/main/lab_1/readme.md'''
    for index, row in df.iterrows():
        if pd.notna(row['Repository Name']):
            urls.append('https://raw.githubusercontent.com/' + row['GitHub Username'] + '/' + row['Repository Name'] + '/' + row['Branch Name'] + '/' + row['Lab Directory Name'] + '/' + row['Readme file name'] )
        else:
            urls.append('https://raw.githubusercontent.com/' + row['GitHub Username'] + '/smart_and_healthy_buildings/' + row['Branch Name'] + '/' + row['Lab Directory Name'] + '/' + row['Readme file name'] )
    return urls

def getContent():
    urls = buildUrl()
    text_array = []
    for url in urls:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, "lxml")
        text = soup.get_text().lstrip().rstrip()
        lines = [s for s in text.splitlines() if s]
        text_array.append(lines)
#        text_array.append([os.linesep.join([s for s in text.splitlines() if s])])
    return text_array
    
def main():
    content = getContent()
    for studentData in content:
        print(studentData) #super inconsistent data, needs manual cleaning
        
        
    
if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# csvdataconvert.py
# ----------------------------------------------------------------------------
# Author: Nicholas Price
# Last Modified: 4/3/2023
# version '1.0.0'
# ---------------------------------------------------------------------------
# Description
# This file is used for the conversion of csv files to data in the code and vice
# versa. 
# ---------------------------------------------------------------------------

import csv


# Description: Take statistics for each player and output their results in a .csv file
# players   : Dictionary    : key, value pairs contain player ID and their lifetime statistics
def convertPlayerDataToCSV(players):
    print('Converting data to CSV')
    header = sorted(list(dict(list(players.values())[0]).keys()))
    data = []

    for p in players:
        temp = dict(sorted(dict(players[p]).items()))
        data.append(list(temp.values()))
    
    print('Writing to CSV file')
    with open('2014hubdata.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    print('Write to', f ,'complete')


# Description: Take the data stored in a .csv file and convert it to a player dictionary
# players   : Dictionary    : key, value pairs contain player ID and their lifetime statistics
def convertCSVToPlayerData(filename):
    players = {}

    # write later #

    return players
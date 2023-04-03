#!/usr/bin/env python3
# csvdataconvert.py
# ----------------------------------------------------------------------------
# Author: Nicholas Price
# Last Modified: 4/4/2023
# version '1.0.0'
# ---------------------------------------------------------------------------
# Description
# This file is used for the conversion of csv files to data in the code and vice
# versa. 
# ---------------------------------------------------------------------------

import csv


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
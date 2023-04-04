#!/usr/bin/env python3
# faceit.py
# ----------------------------------------------------------------------------
# Author: Nicholas Price
# Last Modified: 4/3/2023
# version '1.0.0'
# ---------------------------------------------------------------------------
# Description
# This file is the main driver for the scraping of 2014 CSGO hub data. A
# session is first established with the faceit API. From there calls are made
# to the API to retrieve hub match data. The data is parsed for each player
# and the final result is inserted into a CSV and saved to the 2014FACEIT folder.
# ---------------------------------------------------------------------------

import requests
import config, endpoints, csvdataconvert, faceit

if __name__ == '__main__':
    # Establish a session #
    headers = {
        'accept': 'application/json',
        'Authorization': config.bPlusKey
    }

    # Instantiate a session object #
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(endpoints.faceitapi + '/games?offset=0&limit=0')
    if not response.status_code == 200:
        print("Authentication not successful")
        quit()
    
    # Players dictionary is used to return total statistics based on faceit query type #
    players = {}

    faceit.getHubMatches(endpoints.faceit2014hubID, players, session)

    # Final processing to send player data to a csv file #
    csvdataconvert.convertPlayerDataToCSV(players)
#!/usr/bin/env python3
# endpoints.py
# ----------------------------------------------------------------------------
# Author: Nicholas Price
# Last Modified: 4/3/2023
# version '1.0.0'
# ---------------------------------------------------------------------------
# Description
# This file documents the endpoints interacted with. The main purpose of this
# documentation is to allow for easy changes for any API updates or to
# add/subtract endpoints in the future. 
# ---------------------------------------------------------------------------

faceit2014hub = '6439e8de-340a-4325-b02f-9fe1758b9de8'

faceitapi = 'https://open.faceit.com/data/v4'

##### Hubs #####
# Retrieve hub details
hubs = faceitapi + '/hubs/' + faceit2014hub
# Retrieve all matches of a hub
hubMatches = hubs + '/matches'
# Retrieve all members of a hub
hubMembers = hubs + '/members'
# Retrieve statistics of a hub
hubStats = hubs + '/stats'

##### Matches #####
# Retrieve match details
matches = faceitapi + '/matches'
# Retrieve Match Statistics
def matchStats(match):
    return matches + '/' + match + '/stats'

##### Players #####
# Retrieve player details
player = faceitapi + '/players'
# Retrieve player details
def playerByID(playerID):
    return player + '/' + playerID

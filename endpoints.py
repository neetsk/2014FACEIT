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
def getHubDetails(hubID=faceit2014hub):
    return faceitapi + '/hubs/' + hubID
# Retrieve all matches of a hub
def getHubMatches(hubID):
    return getHubDetails(hubID) + '/matches'
# Retrieve all members of a hub
def getHubMembers(hubID):
    return getHubDetails(hubID) + '/members'
# Retrieve statistics of a hub
def getHubStatistics(hubID):
    return getHubDetails(hubID) + '/stats'

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

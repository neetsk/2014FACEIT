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

import endpoints

# List of the stats we care to calculate from match data (potential conflict with final stats in csv vs player data we scrub from matches)
statList = ['Kills', 'Assists', 'Quadro Kills', 'MVPs', 'Headshots', 'Penta Kills', 'Triple Kills', 
                    'Deaths', 'Rounds Won', 'Rounds Played', 'Games Won', 'Games Played']


# Description: Take statistics from a player's match and update their lifetime statistics based on
#   their player ID.
# stats     : Dictionary    : key, value pairs contain player data from a match
# players   : Dictionary    : key, value pairs contain player ID and their lifetime statistics
# playerID  : String        : the faceit ID of the player to update
def addToPlayerData(stats, players, playerID):
    # If the player already exists in the dictionary, add their stats
    # Else add the player to the dictionary
    if playerID in players:
        # Add stats based on the statList
        for i in range(len(statList)):
            players[playerID][statList[i]] = int(players[playerID][statList[i]]) + int(stats[statList[i]])
    else:
        players[playerID] = stats
    return players


# Description: Process a team's player data and return the updated players dictionary containing
#   universal statistics for the player in the hub 
# teamData  : Dictionary    : key, value pairs contain team specific data and the team_stats key contains player statistics
# numRounds : Int           : the total number of rounds played in the match
# players   : Dictionary    : key, value pairs contain player ID and their lifetime statistics
def processTeamData(teamData, numRounds, players):
    # Assign rounds won and match result to each player
    roundsWon = teamData['team_stats']['Final Score']
    gameWon = teamData['team_stats']['Team Win']
    # Parse data for each player on the team
    for x in teamData['players']:
        playerID = x['player_id']
        stats = x['player_stats']
        # Stats not additive so remove
        stats.pop('K/D Ratio')
        stats.pop('K/R Ratio')
        stats.pop('Headshots %')
        stats.pop('Result')
        # Add in extra stats
        stats['Rounds Won'] = roundsWon
        stats['Rounds Played'] = numRounds
        stats['Games Won'] = gameWon
        stats['Games Played'] = 1
        # Add data collected to current player data
        players = addToPlayerData(stats=stats, players=players, playerID=playerID)
    # return the player data after mutation
    return players


# Description: Process a team's player data and return the updated players dictionary containing
#   universal statistics for the player in the hub 
# teamData  : Dictionary    : key, value pairs contain team specific data and the team_stats key contains player statistics
# numRounds : Int           : the total number of rounds played in the match
# players   : Dictionary    : key, value pairs contain player ID and their lifetime statistics
def processMatchData(matchDataJSON, players):
    if matchDataJSON == None:
        print('Error: No data contained in the matchDataJSON argument of processMatchData')
        quit()
    
    roundsJSON = matchDataJSON['rounds'][0] #modify this to work with multi round games
    numRounds = roundsJSON['round_stats']['Rounds']
    # Scrape stats for both teams in the match
    for teamData in roundsJSON['teams']:
        # could split this into list of dicts of teams and process data that way
        players = processTeamData(teamData=teamData, numRounds=numRounds, players=players)
    return players


# Description: Given a list of all the matches played in a faceit hub, return a
#   dictionary of all the players who haved played and their overall statistics   
# hubMatchesJSON : Dictionary   : key, value pairs contain all match information
# players        : Dictionary   : key, value pairs contain player ID and their lifetime statistics
# session        : Session      : used to authenticate with the api
def processHubMatches(hubMatchesJSON, players, session):
    print('There are', len(hubMatchesJSON['items']), 'matches to process')
    matchSuccessCount = 0
    matchFailedCount = 0

    # For loop to process all matches
    for matchToProcess in hubMatchesJSON['items']:
        matchDataResponse = session.get(endpoints.matchStats(matchToProcess['match_id']))   
        if not matchDataResponse.status_code == 200:
            # Signifies match was not found #
            if matchDataResponse.status_code == 404:
                print(matchToProcess['match_id'], ': failed to process match [', matchDataResponse.status_code, ']')
                matchFailedCount += 1
            else:
                print('Error getting match data, not cancelled or successful', matchDataResponse.status_code, '\n')
                quit()
        else:
            # Match was found so now we scrape data
            players = processMatchData(matchDataJSON=matchDataResponse.json(), players=players)
            matchSuccessCount += 1
            print(matchToProcess['match_id'], ': successfully processed match [', matchDataResponse.status_code, ']')

    # Final amount of matches processed
    print(matchSuccessCount, 'matches successfully processed')
    print(matchFailedCount, 'matches failed to process')
    return players


# Description: This function seeks to add each up to date nickname to the players
#   data. 
# players   : Dictionary   : key, value pairs contain player ID and their lifetime statistics
# session   : Session      : used to authenticate with the api
def addPlayerNicknamesToDict(players, session):
    # Loop to add the current player nicknames to the players dictionary
    for p in players:
        playerData = session.get(endpoints.playerByID(p))
        if not playerData.status_code == 200:
            print('Error retrieving player nickname', playerData.status_code, '\n')
            quit()
        else:
            players[p]['username'] = playerData.json()['nickname']
    # Return with nicknames added to dict        
    return players


# Description: Given a hub ID, process all of the match data from every match played in the hub and return a
#   dictionary of all the players who haved played and their overall statistics  
# hubID     : String        : the unique ID of the faceit hub
# players   : Dictionary    : key, value pairs contain player ID and their lifetime statistics
# session   : Session       : used to authenticate with the api
# offset    : Int           : the number of matches you want to skip processing for
# limit     : Int           : the number of matches you want to process at most
def getHubMatches(hubID, players, session, offset=0, limit=42069):
    params = {
        'offset': offset,
        'limit': limit
    }

    # Hit the hub matches endpoint to retrieve all hub matches #
    hubMatchesResponse = session.get(endpoints.getHubMatches(hubID), params=params)
    if not hubMatchesResponse.status_code == 200:
        print('Error getting hub matches with error code', hubMatchesResponse.status_code, '\n')
        quit()
    
    players = processHubMatches(hubMatchesJSON=hubMatchesResponse.json(), players=players, session=session)
    players = addPlayerNicknamesToDict(players=players, session=session)
    return players


# Description: Given a hub ID, process all of the match data from every match played in the hub and return a
#   dictionary of all the players who haved played and their overall statistics 
# hubID     : String    : the unique ID of the faceit hub 
# session   : Session   : used to authenticate with the api
def printHubMembersInfo(hubID, session):
    response = session.get(endpoints.getHubMembers(hubID))
    if not response.status_code == 200:
        print('Error getting members with error code', response.status_code, '\n')
    else:
        print(response.json())
    return
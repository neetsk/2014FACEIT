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
import config
import endpoints
import csvdataconvert


# Description: Take statistics from a player's match and update their lifetime statistics based on
#   their player ID.
# stats     : Dictionary    : key, value pairs contain player data from a match
# players   : Dictionary    : key, value pairs contain player ID and their lifetime statistics
# playerID  : String        : the faceit ID of the player to update
def mutatePlayerData(stats, players, playerID):
    # If the player already exists in the dictionary, add their stats
    # o.w. add the player to the dictionary
    if playerID in players:
        # add stats
        shortcut = players[playerID]
        shortcut['Kills'] = int(shortcut['Kills']) + int(stats['Kills'])
        shortcut['Assists'] = int(shortcut['Assists']) + int(stats['Assists'])
        shortcut['Quadro Kills'] = int(shortcut['Quadro Kills']) + int(stats['Quadro Kills'])
        shortcut['MVPs'] = int(shortcut['MVPs']) + int(stats['MVPs'])
        shortcut['Headshots'] = int(shortcut['Headshots']) + int(stats['Headshots'])
        shortcut['Penta Kills'] = int(shortcut['Penta Kills']) + int(stats['Penta Kills'])
        shortcut['Triple Kills'] = int(shortcut['Triple Kills']) + int(stats['Triple Kills'])
        shortcut['Deaths'] = int(shortcut['Deaths']) + int(stats['Deaths'])
        shortcut['Rounds Won'] = int(shortcut['Rounds Won']) + int(stats['Rounds Won'])
        shortcut['Rounds Played'] = int(shortcut['Rounds Played']) + int(stats['Rounds Played'])
        shortcut['Games Won'] = int(shortcut['Games Won']) + int(stats['Games Won'])
        shortcut['Games Played'] += 1
    else:
        players[playerID] = stats
    return players


# Description: Process a team's player data and return the updated players dictionary containing
#   universal statistics for the player in the hub 
# teamData  : Dictionary    : key, value pairs contain team specific data and the team_stats key contains player statistics
# numRounds : Int           : the total number of rounds played in the match
# players   : Dictionary    : key, value pairs contain player ID and their lifetime statistics
def processMatchData(teamData, numRounds, players):
    if teamData == None:
        print('Error: No data contained in the teamData argument of processMatchData')
        quit()
    
    # Assign rounds won and if the player won to each team
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
        stats['Rounds Won'] = roundsWon
        stats['Rounds Played'] = numRounds
        stats['Games Won'] = gameWon
        stats['Games Played'] = 1
        players = mutatePlayerData(stats, players, playerID)
    return players


# Description: Given a list of all the matches played in a faceit hub, return a
#   dictionary of all the players who haved played and their overall statistics   
# hubMatchesJSON : Dictionary   : key, value pairs contain all match information
def processPlayerData(hubMatchesJSON):
    # Dictionary of all data in hub for each player (player_id : stats)
    players = {}

    print('There are', len(hubMatchesJSON['items']), 'matches to process')
    matchSuccessCount = 0
    matchFailedCount = 0

    # For loop to process all matches
    for matchToProcess in hubMatchesJSON['items']:
        matchDataResponse = s.get(endpoints.matchStats(matchToProcess['match_id']))   
        if not matchDataResponse.status_code == 200:
            # Signifies match was not found #
            if matchDataResponse.status_code == 404:
                print(matchToProcess['match_id'], ': match failed [', matchDataResponse.status_code, ']')
                matchFailedCount += 1
            else:
                print('Error getting match data, not cancelled or successful', matchDataResponse.status_code, '\n')
                quit()
        else:
            # Match was found so now we scrape data
            roundsJSON = matchDataResponse.json()['rounds'][0]
            numRounds = roundsJSON['round_stats']['Rounds']
            # Scrape stats for both teams in the match
            for teamData in roundsJSON['teams']:
                players = processMatchData(teamData, numRounds, players)
            matchSuccessCount += 1
            print(matchToProcess['match_id'], ': successfully processed[', matchDataResponse.status_code, ']')

    # Final amount of matches processed
    print(matchSuccessCount, 'matches successfully processed')
    print(matchFailedCount, 'matches failed to process')
    return players

# Description: Given a hub ID, process all of the match data from every match played in the hub and return a
#   dictionary of all the players who haved played and their overall statistics  
# hubID  : String   : the unique ID of the faceit hub to pull matches from 
# offset : Int      : the number of matches you want to skip processing for
# limit  : Int      : the number of matches you want to process at most
def getHubMatches(hubID, offset=0, limit=42069):
    params = {
        'offset': offset,
        'limit': limit
    }

    # Hit the endpoint to retrieve all hub matches #
    hubMatchesResponse = s.get(endpoints.getHubMatches(hubID), params=params)
    if not hubMatchesResponse.status_code == 200:
        print('Error getting members with error code', hubMatchesResponse.status_code, '\n')
        quit()
    
    players = processPlayerData(hubMatchesResponse.json())

    # Loop to add the current player nicknames to the players dictionary
    for p in players:
        playerData = s.get(endpoints.playerByID(p))
        if not playerData.status_code == 200:
            print('Error retrieving player nicknames', playerData.status_code, '\n')
            quit()
        else:
            players[p]['username'] = playerData.json()['nickname']

    # Final processing to send player data to a csv file #
    #csvdataconvert.convertPlayerDataToCSV(players)
    return
    

def printHubMembers():
    response = s.get(endpoints.hubMembers)
    if not response.status_code == 200:
        print('Error getting members with error code', response.status_code, '\n')
    else:
        #print(response.json())
        print('members')
    return


if __name__ == '__main__':
    # Establish a session #
    headers = {
        'accept': 'application/json',
        'Authorization': config.bPlusKey
    }

    # Instantiate a session object #
    s = requests.Session()
    s.headers.update(headers)
    response = s.get(endpoints.faceitapi + '/games?offset=0&limit=0')
    if not response.status_code == 200:
        print("Authentication not successful")
        quit()
    
    # 
    getHubMatches(endpoints.faceit2014hub)
    return
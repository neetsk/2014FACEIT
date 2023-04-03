import requests
import config
import endpoints
import csv


def get2014HubMatches(limit=42069):
    params = {
        'offset': 0,
        'limit': limit
    }

    # Hit the endpoint to retrieve all 2014 hub matches #
    hubMatches = s.get(endpoints.hubMatches, params=params)
    if not hubMatches.status_code == 200:
        print('Error getting members with error code', hubMatches.status_code, '\n')
        quit()
    
    # Dictionary of all data in hub for each player (player_id : stats)
    players = {}

    print('There are', len(hubMatches.json()['items']), 'matches to process')
    matchSuccessCount = 0
    matchFailedCount = 0

    # For loop to process all matches
    for matchToProcess in hubMatches.json()['items']:
        matchData = s.get(endpoints.matchStats(matchToProcess['match_id']))   
        if not matchData.status_code == 200:
            # Signifies match was not found #
            if matchData.status_code == 404:
                print(matchToProcess['match_id'], ': match failed [', matchData.status_code, ']')
                matchFailedCount += 1
            else:
                print('Error getting match data, not cancelled or successful', matchData.status_code, '\n')
                quit()
        else:
            # Match was found so now we scrape data
            roundsJSON = matchData.json()['rounds'][0]
            numRounds = roundsJSON['round_stats']['Rounds']
            # Scrape stats for both teams in the match
            for y in roundsJSON['teams']:
                # Assign rounds won and if the player won to each team
                roundsWon = y['team_stats']['Final Score']
                gameWon = y['team_stats']['Team Win']
                # Parse data for each player on the team
                for x in y['players']:
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
            print(matchToProcess['match_id'], ': success')
            matchSuccessCount += 1
    # Final amount of matches processed
    print(matchSuccessCount, 'matches successfully processed')
    print(matchFailedCount, 'matches failed to process')

    # Loop to add the current player nicknames to the players dictionary
    for p in players:
        playerData = s.get(endpoints.playerByID(p))
        if not playerData.status_code == 200:
            print('Error retrieving player nicknames', playerData.status_code, '\n')
            quit()
        else:
            players[p]['username'] = playerData.json()['nickname']

    # Final processing to send player data to a csv file #
    header = sorted(list(dict(list(players.values())[0]).keys()))
        
    data = []

    for p in players:
        temp = dict(sorted(dict(players[p]).items()))
        data.append(list(temp.values()))
        
    with open('2014hubdata.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    

def printHubMembers():
    response = s.get(endpoints.hubMembers)
    if not response.status_code == 200:
        print('Error getting members with error code', response.status_code, '\n')
    else:
        #print(response.json())
        print('members')


if __name__ == '__main__':
    ##### Establish a session #####
    headers = {
        'accept': 'application/json',
        'Authorization': config.bKey
    }

    s = requests.Session()
    s.headers.update(headers)
    response = s.get(endpoints.faceitapi + '/games?offset=0&limit=0')
    if not response.status_code == 200:
        print("Authentication not successful")
        quit()
    
    get2014HubMatches()
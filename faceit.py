import requests
import config
import endpoints
import json
import csv

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

    params = {
        'offset': 0,
        'limit': 999 #change to 999
    }
    hubMatches = s.get(endpoints.hubMatches, params=params)
    if not hubMatches.status_code == 200:
        print('Error getting members with error code', hubMatches.status_code, '\n')
    else:
        #1-717ab86d-38ef-47a4-a941-b19ab5b0fa36
        players = {}

        print('There are', len(hubMatches.json()['items']), 'matches to process')
        matchSuccessCount = 0
        matchFailedCount = 0
        for matchToProcess in hubMatches.json()['items']:
            matchData = s.get(endpoints.matchStats(matchToProcess['match_id']))
            if matchData.status_code == 200:
                roundsJSON = matchData.json()['rounds'][0]
                numRounds = roundsJSON['round_stats']['Rounds']

                for y in roundsJSON['teams']:
                    roundsWon = y['team_stats']['Final Score']
                    gameWon = y['team_stats']['Team Win']
                    for x in y['players']:
                        playerID = x['player_id']
                        stats = x['player_stats']
                        stats.pop('K/D Ratio')
                        stats.pop('K/R Ratio')
                        stats.pop('Headshots %')
                        stats.pop('Result')
                        stats['player_id'] = playerID
                        stats['Rounds Won'] = roundsWon
                        stats['Rounds Played'] = numRounds
                        stats['Games Won'] = gameWon
                        stats['Games Played'] = 1
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
                            players[playerID].pop('player_id')
                print(matchToProcess['match_id'], ': success')
                matchSuccessCount += 1
            else:
                ##### Signifies match was cancelled #####
                if matchData.status_code == 404:
                    print(matchToProcess['match_id'], ': match failed [', matchData.status_code, ']')
                    matchFailedCount += 1
        print(matchSuccessCount, 'matches successfully processed')
        print(matchFailedCount, 'matches failed to process')
        #print(players)

        for p in players:
            playerData = s.get(endpoints.playerByID(p))
            if not playerData.status_code == 200:
                print("error")
            else:
                players[p]['username'] = playerData.json()['nickname']

        ##### Final Processing #####
        header = list(dict(list(players.values())[0]).keys())
        data = []
        
        for p in players:
            data.append(list(dict(players[p]).values()))
        
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
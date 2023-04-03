
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


faceit2014hub = '6439e8de-340a-4325-b02f-9fe1758b9de8'

faceitapi = 'https://open.faceit.com/data/v4/'

##### Hubs #####
# Retrieve hub details
hubs = faceitapi + '/hubs/' + faceit2014hub
# Retrieve all matches of a hub
hubMatches = hubs + '/matches'
# Retrieve all members of a hub
hubMembers = hubs + '/members'
# Retrieve statistics of a hub
hubStats = hubs + '/stats'
import requests
import config
import endpoints

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

    response = s.get(endpoints.hubMatches)
    if not response.status_code == 200:
        print('Error getting members with error code', response.status_code, '\n')
    else:
        print(response.json())


def printHubMembers():
    response = s.get(endpoints.hubMembers)
    if not response.status_code == 200:
        print('Error getting members with error code', response.status_code, '\n')
    else:
        print(response.json())
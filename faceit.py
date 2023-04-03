import requests
import config
import endpoints

headers = {
    'Bearer': config.api_key
}

response = requests.get(endpoints.faceitapi, headers=headers);
print(response)

response = requests.get(endpoints.hubMembers)
if not response.status_code == 200:
    print('Error getting members with error code', response.status_code, '\n')
else:
    print(response.json())

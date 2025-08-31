import config
import requests
import json


url = "https://api-ru.iiko.services/api/1/access_token"

headers = {
    'Content-Type': 'application/json'
}

data = {
    "apiLogin": config.IIKO_LOGIN_KEY
}

resp = requests.post(url, headers=headers, json=data)

print(json.dumps(resp.json(), indent=4))
# print(resp.content)
# import urllib.request

# with urllib.request.urlopen('http://127.0.0.1:5000/odooURI/1') as response:
#     html = response.read()
#     print(html)

import requests

url = 'http://127.0.0.1:5000/odooURI/1'

response = requests.get(url)

data = response.json()

print(data)
import requests

url = 'http://localhost:5000/solve'
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
file_raw = open('02-sample.json', 'r').read()
#print(file_raw)
res = requests.post(url, json=file_raw, headers=headers)
if res.ok:
    print(res.text)


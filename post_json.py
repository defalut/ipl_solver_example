import requests
import sys

filename = ''
if len(sys.argv) >= 2:
    filename = sys.argv[1]
else:
    print("No input file specified, using sample data")
    filename = '02-sample.json'

file_raw = open(filename, 'r').read()

url = 'http://localhost:5000/solve'
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
res = requests.post(url, json=file_raw, headers=headers)
if res.ok:
    print(res.text)


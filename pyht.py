import requests
URL = "http://127.0.0.1:5000/getdata"
r = requests.get(url = URL)
data = r.json()
print(data)

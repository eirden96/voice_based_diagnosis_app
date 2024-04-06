import requests
import datetime
import json

url = 'http://localhost:5000/send_data'
files = {'file': open('Trailer.wav', 'rb')}
current_time =  datetime.datetime.now()
data = {"timestamp": str(current_time), "user": "Eirini"}
response = requests.post(url, files=files, data=data)

print(response.text)
print("======")
print(response.status_code)
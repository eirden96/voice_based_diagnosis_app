import requests
import datetime
import json

url = 'http://localhost:5000/send_data'

response = requests.get(f"{url}?user=Eirini")

print(response.text)
print("======")
print(response.status_code)
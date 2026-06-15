from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("Exhange_API_Key")

url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'
response = requests.get(url)
data = response.json()
print(data) 

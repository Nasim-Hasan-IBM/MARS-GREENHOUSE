import os
import requests
from dotenv import load_dotenv

# 1. Load credentials
load_dotenv("Secrets.env")
NASA_API_KEY = os.environ["NASA_API_KEY"]

#2. Consuming NASA's InSight Mars API
resp = requests.get("https://api.nasa.gov/insight_weather/?api_key="+NASA_API_KEY+"&feedtype=json&ver=1.0")
resp.raise_for_status()  # Raises for 4xx/5xx
print(resp.json())
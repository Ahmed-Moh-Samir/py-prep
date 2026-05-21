import requests

url = "https://re.jrc.ec.europa.eu/api/v5_3/seriescalc"

response = requests.get(url)

print(response.json())
import requests
import csv

url = "https://re.jrc.ec.europa.eu/api/v5_3/seriescalc"



params = {
    "lat": 34.7,
    "lon": 33.0,
    "startyear": 2023,
    "endyear": 2023,
    "pvcalculation": 1,
    "peakpower": 5,
    "loss": 14,
    "outputformat": "json"
}

response = requests.get(url , params=params)

if response.status_code == 200:
    data = response.json()
    hourly = data["outputs"]["hourly"]
    
    print("Records returned:", len(hourly))
    print("First record:", hourly[0])
    print("record at noon on a sunny day:", hourly[5000])
    print("Last record:", hourly[-1])
    
    total_watt_hours = sum(record["P"] for record in hourly)
    total_kwh = total_watt_hours / 1000
    print(f"Total energy produced in 2023: {total_kwh:.1f} kWh")
    
    max_hour_w = max(record["P"] for record in hourly)
    print(f"Peak hour: {max_hour_w:.1f} W")
    
    with open("solar_output_2023.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=hourly[0].keys())
        writer.writeheader()
        writer.writerows(hourly)
        
        print("saved data to solar_output_2023.csv")
else:
    print(f"API CALL FAILED WITH STATUS CODE: {response.status_code}")
    print(response.text)
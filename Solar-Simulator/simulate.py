import csv

solar_kWh = []

with open("solar_output_2023.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for i, row in enumerate(csv_reader):
        solar_kWh.append(float(row["P"]) / 1000)
print(f"Records: {len(solar_kWh)}")
print(f"Annual total: {sum(solar_kWh):.1f} kWh")
print(f"Peak hour: {max(solar_kWh):.2f} kWh")
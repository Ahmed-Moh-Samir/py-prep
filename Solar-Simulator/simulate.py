import csv
from consumption import get_consumption
solar_kWh = []

with open("solar_output_2023.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for i, row in enumerate(csv_reader):
        solar_kWh.append(float(row["P"]) / 1000)

print(f"Records: {len(solar_kWh)}")
print(f"Annual total: {sum(solar_kWh):.1f} kWh")
print(f"Peak hour: {max(solar_kWh):.2f} kWh")

solar_direct = 0
solar_exported = 0
grid_imported = 0
consumption_total = 0

for i in range(len(solar_kWh)):
    solar = solar_kWh[i]
    consumption = get_consumption(i % 24)
    if solar >= consumption:
        solar_direct += consumption
        solar_exported += (solar - consumption)
        consumption_total += consumption
    else:
        solar_direct += solar
        grid_imported += (consumption - solar)
        consumption_total += consumption
print()
print(f"Annual consumption:       {consumption_total:.1f} kWh")
print(f"Solar used directly:      {solar_direct:.1f} kWh")
print(f"Solar exported (wasted):  {solar_exported:.1f} kWh")
print(f"Grid imported:            {grid_imported:.1f} kWh")
self_consumption = solar_direct / consumption_total * 100
print(f"Self-consumption (no battery): {self_consumption:.1f} %")

# Sanity checks
print()
print(f"Check: solar_direct + solar_exported = {solar_direct + solar_exported:.1f} "
      f"(should match annual total ~7652)")
print(f"Check: solar_direct + grid_imported = {solar_direct + grid_imported:.1f} "
      f"(should match consumption_total ~4818)")
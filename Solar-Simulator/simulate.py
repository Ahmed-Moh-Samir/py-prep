import csv
import matplotlib.pyplot as plt
from consumption import get_consumption
solar_kWh = []
history_solar = []
history_consumption = []
history_battery = []
history_grid = []

with open("solar_output_2023.csv") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for i, row in enumerate(csv_reader):
        solar_kWh.append(float(row["P"]) / 1000)

print(f"Records: {len(solar_kWh)}")
print(f"Annual total: {sum(solar_kWh):.1f} kWh")
print(f"Peak hour: {max(solar_kWh):.2f} kWh")

battery_capacity = 13.5
charge_rate = 5
battery_charge = 0
solar_to_battery = 0
battery_to_load = 0

solar_direct = 0
solar_exported = 0
grid_imported = 0
consumption_total = 0

for i in range(len(solar_kWh)):
    solar = solar_kWh[i]
    consumption = get_consumption(i % 24)
    if solar >= consumption:
        excess = solar - consumption
        charged = min(excess,charge_rate,battery_capacity - battery_charge) 
        battery_charge += charged
        solar_to_battery += charged
        solar_exported += (excess - charged)   
        solar_direct += consumption
        consumption_total += consumption
        grid_this_hour = 0
    else:
        deficit = consumption - solar
        discharged = min(deficit,charge_rate,battery_charge)
        battery_charge -= discharged
        battery_to_load += discharged
        grid_imported += (deficit - discharged)
        solar_direct += solar
        consumption_total += consumption
        grid_this_hour = deficit - discharged
    
    history_solar.append(solar)
    history_consumption.append(consumption)
    history_battery.append(battery_charge)
    history_grid.append(grid_this_hour)


print(len(history_solar))
print()
print(f"Annual consumption:       {consumption_total:.1f} kWh")
print(f"Solar used directly:      {solar_direct:.1f} kWh")
print(f"Solar to battery:         {solar_to_battery:.1f} kWh")
print(f"Battery to load:          {battery_to_load:.1f} kWh")
print(f"Solar exported (wasted):  {solar_exported:.1f} kWh")
print(f"Grid imported:            {grid_imported:.1f} kWh")
print(f"Battery end-of-year charge: {battery_charge:.2f} kWh")

self_consumption = (solar_direct + battery_to_load) / consumption_total * 100
print(f"Self-consumption (WITH battery): {self_consumption:.1f} %")

# Sanity checks — three-term equations
print()
solar_side = solar_direct + solar_to_battery + solar_exported
load_side = solar_direct + battery_to_load + grid_imported
print(f"Check: solar_direct + solar_to_battery + solar_exported = {solar_side:.1f} "
      f"(should match ~7652)")
print(f"Check: solar_direct + battery_to_load + grid_imported = {load_side:.1f} "
      f"(should match consumption_total ~4818)")

day = 167          # June 17, as a 0-indexed day of the year
start = day * 24   # first hour-index of that day
end = start + 24   # one past the last hour of that day

hours = list(range(24))
day_solar = history_solar[start:end]
day_consumption = history_consumption[start:end]
day_battery = history_battery[start:end]
day_grid = history_grid[start:end]

plt.plot(hours, day_solar, label="Solar production")
plt.plot(hours, day_consumption, label="Consumption")
plt.plot(hours, day_battery, label="Battery charge")
plt.plot(hours, day_grid, label="Grid import")
plt.xlabel("Hour of day")
plt.ylabel("kWh")
plt.title("Representative summer day (June 17)")
plt.legend()
plt.show()
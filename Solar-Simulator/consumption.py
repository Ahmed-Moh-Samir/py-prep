import matplotlib.pyplot as plt

def get_consumption(hour):
    if 0 <= hour < 6:
        return 0.2
    elif 6 <= hour < 9:
        return 0.6
    elif 9 <= hour < 17:
        return 0.4
    elif 17 <= hour < 22:   
        return 1.2
    elif 22 <= hour < 24:
        return 0.5
    else:
        raise ValueError(f"Hour out of range: {hour}")
    
if __name__ == "__main__":
    hours = []
    values = []
    for hour in range(24):
        consumption = get_consumption(hour)
        hours.append(hour)
        values.append(consumption)
        print(f"Hour {hour}: consumption = {consumption} kWh")
    total = sum(values)
    print(f"Daily total: {total:.1f} kWh")

    plt.plot(hours, values)
    plt.xlabel("Hour of day")
    plt.ylabel("consumtion (kWh)")
    plt.title("Household daily load")
    plt.show()
# Solar Self-Consumption Simulator

A Python simulation that models a household with rooftop solar and a battery in
Limassol, Cyprus, and quantifies how much of the home's yearly electricity could
come from solar rather than the grid.

The headline result: adding a 13.5 kWh battery to a 5 kW solar array raises
self-consumption from **34.6% to 96.5%**, cutting annual grid imports by roughly
**95%** (from ~3151 kWh to ~171 kWh).

## Motivation

Cyprus has some of the strongest solar resources in Europe, but most solar
generation lands at midday — when a typical household is using very little
electricity. The household's real demand peaks in the evening, after the sun has
set. This timing mismatch means a lot of solar is wasted unless it can be stored.

This project quantifies that mismatch and measures how much of it a home battery
can close, using real hourly solar data rather than rules of thumb.

## What it does

1. Fetches a full year (2023) of hourly solar production data for Limassol from
   the PVGIS API (European Commission Joint Research Centre) and caches it to CSV.
2. Models a household's hourly electricity consumption using a time-of-day load
   profile (~13.2 kWh/day).
3. Simulates, hour by hour across all 8760 hours of the year, how solar,
   consumption, a battery, and the grid interact.
4. Reports annual totals and self-consumption percentages, with and without the
   battery.
5. Plots a representative day showing solar production, consumption, battery
   state of charge, and grid import.

## How to run

Requirements: Python 3.12, `requests`, `matplotlib`.

```
pip install requests matplotlib
```

Step 1 — fetch and cache the solar data (only needs to run once):

```
cd Solar-Simulator
python solar-simulator.py
```

This writes `solar_output_2023.csv` to the project folder.

Step 2 — run the simulation and produce the chart:

```
python simulate.py
```

The script prints the annual summary to the terminal and opens a matplotlib
window with the representative-day chart.

## How it works

### Data source

Solar production comes from the PVGIS `seriescalc` endpoint, which returns hourly
PV output (in watts) for a given location and array size. No API key or
registration is required. The query uses:

| Parameter | Value | Meaning |
|---|---|---|
| `lat`, `lon` | 34.7, 33.0 | Limassol, Cyprus |
| `peakpower` | 5 | 5 kW solar array |
| `loss` | 14 | Standard 14% system losses |
| `startyear`, `endyear` | 2023 | One full year |

### Consumption model

A fixed time-of-day profile (kWh per hour):

| Hours | kWh/hour |
|---|---|
| 00:00–06:00 | 0.2 |
| 06:00–09:00 | 0.6 |
| 09:00–17:00 | 0.4 |
| 17:00–22:00 | 1.2 |
| 22:00–24:00 | 0.5 |

This totals 13.2 kWh/day (4818 kWh/year).

### Battery model

- Capacity: 13.5 kWh
- Maximum charge/discharge rate: 5 kW
- Round-trip efficiency: 100% (see limitations)

Each hour, the simulation compares solar production to consumption. Surplus solar
charges the battery (up to its capacity and charge rate); any remaining surplus is
exported. When consumption exceeds solar, the battery discharges to cover the gap
(up to its charge level and discharge rate); any remaining shortfall is imported
from the grid.

## Results

For a 5 kW array and 13.5 kWh battery in Limassol over 2023:

| Metric | Without battery | With battery |
|---|---|---|
| Self-consumption | 34.6% | 96.5% |
| Grid imported | 3151 kWh | 171 kWh |
| Solar exported (wasted) | 5985 kWh | 3005 kWh |

The battery moves about 2980 kWh of solar from midday surplus to evening use over
the year — roughly 220 full charge/discharge cycles. Even with the battery, about
3000 kWh of summer surplus is still exported, because the battery fills by midday
and has nowhere to put the rest.

## Limitations

This is a v1 model and is deliberately simplified. Real-world results would be
somewhat lower than the figures above. Known simplifications:

- **Battery efficiency is assumed to be 100%.** Real lithium-ion batteries lose
  roughly 10% on a round trip, so true self-consumption would be a few points
  lower.
- **Consumption is a fixed daily profile.** A real household varies day to day and
  season to season (summer air conditioning, winter heating), which this model
  does not capture.
- **No battery degradation.** Real battery capacity falls ~2% per year.
- **No feed-in tariff.** Exported solar is treated as wasted; in markets that pay
  for exports, the economics would differ.
- **One year of data (2023).** Year-to-year weather variation is not averaged out.

## Possible extensions

- Model battery efficiency and state-of-charge limits.
- Compare different battery and array sizes.
- Add a financial model (payback period at Cyprus electricity prices).
- Use a multi-year or typical-meteorological-year dataset.
- Add a deferrable load (water heater or EV charging) to capture midday surplus.

## Data attribution

Solar data from the Photovoltaic Geographical Information System (PVGIS),
European Commission Joint Research Centre.
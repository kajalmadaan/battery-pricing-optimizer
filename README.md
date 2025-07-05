# Battery Optimization Simulation

A simple Python model simulating battery charging/discharging behavior based on:
- Hourly demand
- Grid electricity price variations
- Fixed selling price to customers

## Features

- Models profit based on battery use vs direct grid use.
- Compares different battery sizes (e.g. 10 kWh vs 60 kWh).
- Illustrates profitability over 24 hours.

## To Run

```bash
pip install matplotlib numpy scikit-learn
python battery_optimizer.py

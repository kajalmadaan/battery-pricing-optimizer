#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Battery Optimization Simulation
Created on June 21, 2025

@author: kajalmadaan
"""

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Setup & Simulation Parameters
# ----------------------------

np.random.seed(100)  # For reproducibility

battery_sizes = [10, 60]  # Battery capacity options (kWh)
energy_demand = np.random.uniform(1, 5, 24)  # Simulated hourly demand (kWh)

# Electricity grid cost profile (€/kWh)
grid_price = [0.10 if h < 8 or h > 20 else 0.30 for h in range(24)]

# Fixed customer selling price (€/kWh)
selling_price = [0.29] * 24

# ----------------------------
# Simulation Function
# ----------------------------

def simulate(battery_capacity):
    battery_level = 0
    cost = 0
    revenue = 0
    hourly_profit = []

    for hour in range(24):
        demand = energy_demand[hour]
        grid_cost = grid_price[hour]
        sell_price = selling_price[hour]

        # Charge battery during low-cost hours
        if grid_cost == 0.10 and battery_level < battery_capacity:
            charge = min(battery_capacity - battery_level, 5)
            battery_level += charge
            cost += charge * grid_cost

        # Discharge battery to meet demand
        if battery_level >= demand:
            battery_level -= demand
            revenue += demand * sell_price
        else:
            from_grid = demand - battery_level
            revenue += demand * sell_price
            cost += from_grid * grid_cost
            battery_level = 0

        hourly_profit.append(revenue - cost)

    return hourly_profit, round(revenue - cost, 2)

# ----------------------------
# Run & Plot Results
# ----------------------------

plt.figure(figsize=(5, 2.5))

for size in battery_sizes:
    profits, total = simulate(size)
    print(f"Battery Size: {size} kWh — Total Profit: {total} €")
    plt.plot(profits, label=f"{size} kWh")

plt.title("Cumulative Profit Over 24h")
plt.xlabel("Hour")
plt.ylabel("Cumulative Profit (€)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Example training data: [hour of day, temperature, weekday] → demand
X_train = np.array([
    [9, 22, 1], [12, 30, 1], [18, 27, 1], 
    [9, 15, 0], [12, 18, 0], [18, 20, 0]
])
y_train = np.array([20, 35, 50, 15, 30, 45])  # Historical demand values (kWh)

model = LinearRegression()
model.fit(X_train, y_train)

# Predict demand for current conditions
now = datetime.now()
current_hour = now.hour
temperature = 25  # Example temperature
weekday = 1 if now.weekday() < 5 else 0

X_pred = np.array([[current_hour, temperature, weekday]])
predicted_demand = model.predict(X_pred)[0]


def compute_dynamic_price(grid_cost, demand, competitors):
    base_price = grid_cost + 0.10  # margin
    demand_surcharge = 0.01 * (demand - 20)  # markup if demand is high
    competitive_discount = 0.05 if competitors < 3 else 0.00
    return round(base_price + demand_surcharge - competitive_discount, 2)

grid_cost = 0.12  # €/kWh
competitors = 2

price = compute_dynamic_price(grid_cost, predicted_demand, competitors)


def compute_battery_action(price, soc, grid_status):
    if soc < 30 and grid_status == "off-peak":
        return "charge"
    elif soc > 70 and price > 0.25:
        return "discharge"
    else:
        return "standby"

battery_soc = 50  # battery state of charge in %
grid_status = "peak"  # could be real-time from grid API

battery_action = compute_battery_action(price, battery_soc, grid_status)


print(f"Predicted Demand: {predicted_demand:.2f} kWh")
print(f"Dynamic Price: €{price}/kWh")
print(f"Battery Action: {battery_action}")

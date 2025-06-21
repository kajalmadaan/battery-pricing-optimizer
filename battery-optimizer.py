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

# SPDX-FileCopyrightText: 2019 Mikey Sklar for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import csv, statistics

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)

print('Raw ADC Value: ', chan0.value)
print('ADC Voltage: ' + str(chan0.voltage) + 'V')

def read_voltage(samples=30, delay=0.01):
    vals = []
    for _ in range(samples):
        vals.append(chan0.voltage)
        time.sleep(delay)
    return statistics.median(vals)


distances = []
voltages = []

print("Calibration mode. Place object, then type distance in cm.")
print("Press Enter with no input when finished.\n")


while True:
    print("-----------------------------")

    user_input = input("Enter distance (cm): ").strip()
    if user_input == "":
        break
    try:
        dist = float(user_input)
    except ValueError:
        print("Invalid input. Try again.")
        continue
    
    # read the analog pin
    v = read_voltage()
    print(f"Measured median voltage: {v:.3f} V\n")
    distances.append(dist)
    voltages.append(v)

    # hang out and do nothing for a half second
    time.sleep(0.5)


# Save data
with open("calibration_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Distance_cm", "Voltage_V"])
    writer.writerows(zip(distances, voltages))
print("Data saved to calibration_data.csv")

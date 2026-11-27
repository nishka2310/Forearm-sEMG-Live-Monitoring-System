
import pandas as pd
import matplotlib.pyplot as plt

# Load recorded data
data = pd.read_csv("EMG_Raw_Data.csv")

samples = data["Sample"]
signal = data["ADC_Value"]

# Remove the average baseline for easier viewing
centered_signal = signal - signal.mean()

plt.figure(figsize=(12, 5))
plt.plot(samples, signal, linewidth=0.8)
plt.title("Raw Sensor Signal")
plt.xlabel("Sample Number")
plt.ylabel("ADC Value")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 5))
plt.plot(samples, centered_signal, linewidth=0.8)
plt.title("Baseline-Centered Sensor Signal")
plt.xlabel("Sample Number")
plt.ylabel("ADC Value - Mean")
plt.grid(True)
plt.tight_layout()
plt.show()

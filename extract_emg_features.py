
import pandas as pd
import numpy as np

data = pd.read_csv("EMG_Raw_Data.csv")
signal = data["ADC_Value"].astype(float)

# Remove baseline
signal = signal - signal.mean()

# Basic features
mav = np.mean(np.abs(signal))
rms = np.sqrt(np.mean(signal ** 2))
variance = np.var(signal)
std_dev = np.std(signal)
waveform_length = np.sum(np.abs(np.diff(signal)))

print("EMG Feature Extraction")
print("----------------------")
print("Total samples:", len(signal))
print("MAV:", round(mav, 3))
print("RMS:", round(rms, 3))
print("Variance:", round(variance, 3))
print("Standard Deviation:", round(std_dev, 3))
print("Waveform Length:", round(waveform_length, 3))

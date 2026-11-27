
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfiltfilt

data = pd.read_csv("EMG_Raw_Data.csv")
signal = data["ADC_Value"].astype(float)

# Remove DC baseline
centered = signal - signal.mean()

# Sampling frequency must match actual acquisition rate.
# Use 500 Hz only if your Arduino sampling is verified at 500 Hz.
fs = 500

# Bandpass filter: 20–200 Hz
sos = butter(
    4, [20, 200],
    btype="bandpass",
    fs=fs,
    output="sos"
)

filtered = sosfiltfilt(sos, centered)

plt.figure(figsize=(12, 5))
plt.plot(data["Sample"], centered, label="Raw centered signal",
         alpha=0.5)
plt.plot(data["Sample"], filtered, label="Filtered signal")
plt.xlabel("Sample Number")
plt.ylabel("Amplitude (ADC counts)")
plt.title("Raw vs Filtered Signal")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

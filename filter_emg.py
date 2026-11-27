
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfiltfilt

# Load sensor-test data
data = pd.read_csv("EMG_Raw_Data.csv")
signal = data["ADC_Value"].astype(float)

# Remove the DC baseline
centered = signal - signal.mean()

# Temporary exploratory filter only.
# Sampling rate is NOT verified yet.
# Do not treat this as validated EMG filtering.
fs = 500
lowcut = 20
highcut = 200

sos = butter(
    4,
    [lowcut, highcut],
    btype="bandpass",
    fs=fs,
    output="sos"
)

filtered = sosfiltfilt(sos, centered)

plt.figure(figsize=(12, 5))
plt.plot(data["Sample"], centered, label="Baseline-centered")
plt.plot(data["Sample"], filtered, label="Filtered", alpha=0.8)
plt.xlabel("Sample number")
plt.ylabel("Signal (ADC counts)")
plt.title("Sensor-test data: before vs after filtering")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

data["Centered_ADC"] = centered
data["Filtered_Test"] = filtered
data.to_csv("EMG_Filtered_Test.csv", index=False)

print("Saved: EMG_Filtered_Test.csv")
print("Note: filter settings are exploratory, not validated.")

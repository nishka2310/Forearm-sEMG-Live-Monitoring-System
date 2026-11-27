
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load recorded CSV files
rest = pd.read_csv("rest.csv")
contraction = pd.read_csv("contraction.csv")

# Extract ADC readings and remove the baseline offset
rest_signal = rest["ADC_Value"].astype(float).to_numpy()
contraction_signal = contraction["ADC_Value"].astype(float).to_numpy()

rest_signal = rest_signal - np.mean(rest_signal)
contraction_signal = contraction_signal - np.mean(contraction_signal)

# Calculate signal features
def calculate_features(signal):
    mav = np.mean(np.abs(signal))
    rms = np.sqrt(np.mean(signal ** 2))
    return mav, rms

rest_mav, rest_rms = calculate_features(rest_signal)
contraction_mav, contraction_rms = calculate_features(contraction_signal)

print("REST")
print(f"MAV: {rest_mav:.3f}")
print(f"RMS: {rest_rms:.3f}")

print("\nCONTRACTION")
print(f"MAV: {contraction_mav:.3f}")
print(f"RMS: {contraction_rms:.3f}")

# Plot both signals
plt.figure(figsize=(12, 5))
plt.plot(rest_signal, linewidth=0.7)
plt.title("Forearm sEMG - Rest")
plt.xlabel("Sample Number")
plt.ylabel("Centered ADC Counts")
plt.grid(True)
plt.tight_layout()
plt.savefig("rest_signal.png", dpi=200)
plt.show()

plt.figure(figsize=(12, 5))
plt.plot(contraction_signal, linewidth=0.7)
plt.title("Forearm sEMG - Contraction")
plt.xlabel("Sample Number")
plt.ylabel("Centered ADC Counts")
plt.grid(True)
plt.tight_layout()
plt.savefig("contraction_signal.png", dpi=200)
plt.show()

# Compare rest and contraction
plt.figure(figsize=(7, 5))
plt.bar(
    ["Rest", "Contraction"],
    [rest_rms, contraction_rms]
)
plt.title("RMS Comparison: Rest vs Contraction")
plt.ylabel("RMS (ADC Counts)")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("rest_vs_contraction.png", dpi=200)
plt.show()

print("\nPlots saved successfully.")

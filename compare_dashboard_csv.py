
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

root = Tk()
root.withdraw()

print("Select REST CSV file")
rest_file = filedialog.askopenfilename(
    title="Select REST CSV",
    filetypes=[("CSV files", "*.csv")]
)

print("Select CONTRACTION CSV file")
contraction_file = filedialog.askopenfilename(
    title="Select CONTRACTION CSV",
    filetypes=[("CSV files", "*.csv")]
)

root.destroy()

if not rest_file or not contraction_file:
    print("Please select both CSV files.")
    raise SystemExit

rest = pd.read_csv(rest_file)
contraction = pd.read_csv(contraction_file)

# Remove the average ADC level to compare signal activity
rest_signal = rest["ADC_Value"] - rest["ADC_Value"].mean()
contraction_signal = (
    contraction["ADC_Value"] - contraction["ADC_Value"].mean()
)

def features(signal):
    return {
        "MAV": signal.abs().mean(),
        "RMS": (signal.pow(2).mean()) ** 0.5,
        "Peak-to-Peak": signal.max() - signal.min()
    }

rest_features = features(rest_signal)
contraction_features = features(contraction_signal)

print("\nREST FEATURES:", rest_features)
print("CONTRACTION FEATURES:", contraction_features)

fig, axes = plt.subplots(2, 1, figsize=(10, 7))

axes[0].plot(rest_signal)
axes[0].set_title("Forearm sEMG - Rest")
axes[0].set_ylabel("Centred ADC Value")

axes[1].plot(contraction_signal)
axes[1].set_title("Forearm sEMG - Contraction")
axes[1].set_ylabel("Centred ADC Value")
axes[1].set_xlabel("Sample")

plt.tight_layout()
plt.show()

pd.DataFrame({
    "Feature": list(rest_features.keys()),
    "Rest": list(rest_features.values()),
    "Contraction": list(contraction_features.values())
}).to_csv("semg_comparison_results.csv", index=False)

print("Comparison results saved.")

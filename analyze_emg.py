
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

folder = Path(__file__).resolve().parent

for label, filename in [
    ("Rest", "rest.csv"),
    ("Contraction", "contraction.csv")
]:
    path = folder / filename

    if not path.exists():
        print(f"File not found: {path}")
        continue

    df = pd.read_csv(path)
    print(f"\n{label} columns: {list(df.columns)}")

    if "adc_value" in df.columns:
        signal = df["adc_value"].dropna().astype(float).to_numpy()
    elif "value" in df.columns:
        signal = df["value"].dropna().astype(float).to_numpy()
    else:
        print("ADC column not found. Check the column names above.")
        continue

    if len(signal) == 0:
        print(f"No samples in {filename}")
        continue

    centered = signal - np.mean(signal)
    mav = np.mean(np.abs(centered))
    rms = np.sqrt(np.mean(centered ** 2))

    print(f"Samples: {len(signal)}")
    print(f"MAV: {mav:.3f}")
    print(f"RMS: {rms:.3f}")

    plt.figure(figsize=(10, 4))
    plt.plot(signal)
    plt.title(f"{label} Forearm Signal")
    plt.xlabel("Sample number")
    plt.ylabel("ADC counts")
    plt.grid(True)
    plt.tight_layout()

    output = folder / f"{label.lower()}_plot.png"
    plt.savefig(output, dpi=150)
    print(f"Graph saved to: {output}")

    plt.show()

print("\nAnalysis finished.")


import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("EMG_Timestamped_Test.csv")

print("Total samples:", len(df))
print("Minimum:", df["ADC_Value"].min())
print("Maximum:", df["ADC_Value"].max())
print("Mean:", round(df["ADC_Value"].mean(), 2))
print("Standard deviation:", round(df["ADC_Value"].std(), 2))

time_sec = (
    df["Timestamp_us"] - df["Timestamp_us"].iloc[0]
) / 1_000_000

plt.figure(figsize=(12, 5))
plt.plot(time_sec, df["ADC_Value"])
plt.title("Sensor Test Data")
plt.xlabel("Time (seconds)")
plt.ylabel("ADC Value")
plt.grid(True)
plt.tight_layout()
plt.show()

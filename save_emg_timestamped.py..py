
import serial
import pandas as pd
import time

PORT = "COM10"
BAUD = 115200

rows = []

try:
    with serial.Serial(PORT, BAUD, timeout=2) as ser:
        print("Waiting for Arduino data...")
        time.sleep(2)
        ser.reset_input_buffer()

        while True:
            line = ser.readline().decode(
                "utf-8", errors="ignore"
            ).strip()

            if line == "Recording complete":
                break

            if not line or line.startswith("Timestamp_us"):
                continue

            parts = line.split(",")

            if len(parts) == 2:
                try:
                    timestamp = int(parts[0])
                    adc_value = int(parts[1])
                    rows.append([timestamp, adc_value])
                    print(timestamp, adc_value)
                except ValueError:
                    pass

    df = pd.DataFrame(
        rows,
        columns=["Timestamp_us", "ADC_Value"]
    )
    df.to_csv("EMG_Timestamped_Test.csv", index=False)

    print(f"\nSaved {len(df)} samples.")
    print("File: EMG_Timestamped_Test.csv")

except serial.SerialException as e:
    print("Serial port error:", e)


import serial
import csv
import time

PORT = "COM10"
BAUD_RATE = 115200
DURATION = 30  # seconds

with serial.Serial(PORT, BAUD_RATE, timeout=2) as arduino:
    time.sleep(2)

    with open("EMG_Raw_Data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Sample", "ADC_Value"])

        start_time = time.time()
        count = 0

        print("Recording started...")

        while time.time() - start_time < DURATION:
            line = arduino.readline().decode(
                "utf-8", errors="ignore"
            ).strip()

            parts = line.split(",")

            if len(parts) == 2:
                try:
                    sample = int(parts[0])
                    value = int(parts[1])

                    writer.writerow([sample, value])
                    count += 1
                except ValueError:
                    continue

    print(f"Recording complete! Samples saved: {count}")
    print("File: EMG_Raw_Data.csv")

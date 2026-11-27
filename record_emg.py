
import serial
import csv
import time

PORT = "COM10"
BAUD = 115200
NUM_SAMPLES = 2000

def record_emg(condition, filename):
    input(
        f"\nPrepare your forearm for {condition.upper()}.\n"
        "Press ENTER when ready to start recording..."
    )

    ser = serial.Serial(PORT, BAUD, timeout=2)
    time.sleep(2)

    # Reset Arduino so its 2000-sample recording starts again
    ser.reset_input_buffer()

    count = 0

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Sample", "Time_ms", "ADC_Value"])

        while count < NUM_SAMPLES:
            line = ser.readline().decode(
                "utf-8", errors="ignore"
            ).strip()

            parts = line.split(",")

            # Expected Arduino format:
            # Sample,Time_ms,ADC_Value
            if len(parts) == 3 and parts[0].isdigit():
                writer.writerow(parts)
                count += 1
                print(
                    f"{condition}: {count}/{NUM_SAMPLES} samples",
                    end="\r"
                )

    ser.close()
    print(f"\nSaved {count} samples to {filename}")


print("FOREARM sEMG DATA RECORDING")
print("Arduino must be running the 2000-sample code.")
print("Close Arduino Serial Monitor before continuing.")

record_emg("Rest", "rest.csv")
record_emg("Contraction", "contraction.csv")

print("\nBoth recordings are complete!")
print("Files saved: rest.csv and contraction.csv")

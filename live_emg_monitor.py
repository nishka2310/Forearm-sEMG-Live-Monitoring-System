
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import numpy as np
import time

# Change COM10 if your Arduino uses another port
PORT = "COM10"
BAUD_RATE = 115200

WINDOW_SIZE = 100
THRESHOLD = 6.0  # Adjust after observing your signals

ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)
ser.reset_input_buffer()

samples = deque([0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)
sample_number = deque(range(WINDOW_SIZE), maxlen=WINDOW_SIZE)

fig, ax = plt.subplots(figsize=(10, 5))
line, = ax.plot(list(sample_number), list(samples),
                label="EMG Signal")

ax.set_title("Real-Time Forearm sEMG Monitor")
ax.set_xlabel("Recent Samples")
ax.set_ylabel("Arduino ADC Value")
ax.set_ylim(0, 1023)
ax.grid(True)

status_text = ax.text(
    0.02, 0.93, "Waiting for signal...",
    transform=ax.transAxes, fontsize=12
)
rms_text = ax.text(
    0.02, 0.86, "RMS: --",
    transform=ax.transAxes, fontsize=11
)

def update(frame):
    global samples

    # Read incoming sensor values
    for _ in range(50):
        try:
            raw = ser.readline().decode(
                "utf-8", errors="ignore"
            ).strip()

            if raw.isdigit():
                samples.append(int(raw))

        except (ValueError, serial.SerialException):
            pass

    values = np.array(samples, dtype=float)
    centered = values - np.mean(values)

    # RMS of the centered signal window
    rms = np.sqrt(np.mean(centered ** 2))

    line.set_ydata(values)
    line.set_xdata(range(len(values)))

    rms_text.set_text(f"RMS: {rms:.2f} ADC counts")

    if rms >= THRESHOLD:
        status_text.set_text("HIGH ACTIVITY")
    else:
        status_text.set_text("LOW ACTIVITY")

    ax.set_xlim(0, WINDOW_SIZE - 1)

    return line, status_text, rms_text

ani = FuncAnimation(
    fig, update, interval=100,
    blit=False, cache_frame_data=False
)

try:
    plt.tight_layout()
    plt.show()
finally:
    ser.close()

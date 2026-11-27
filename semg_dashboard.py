
import csv
import time
from datetime import datetime
from collections import deque

import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from tkinter import Tk, filedialog, messagebox

# ---------- SETTINGS ----------
PORT = "COM10"
BAUD_RATE = 115200
WINDOW_SIZE = 100
THRESHOLD = 6.0
UPDATE_INTERVAL = 100  # milliseconds

# ---------- SERIAL CONNECTION ----------
try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=0.01)
except serial.SerialException as error:
    raise SystemExit(
        f"Cannot open {PORT}.\n"
        "Close Arduino Serial Monitor/Plotter and check the COM port.\n"
        f"Details: {error}"
    )

# Arduino UNO may reset when the serial port opens
time.sleep(2)
ser.reset_input_buffer()

# ---------- DATA ----------
signal = deque([0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)
recorded_rows = []
byte_buffer = bytearray()

recording = False
recording_start = None
sample_count = 0
current_rms = 0.0
current_status = "LOW ACTIVITY"

# ---------- DASHBOARD ----------
fig, ax = plt.subplots(figsize=(11, 7))
plt.subplots_adjust(bottom=0.25, top=0.88)

fig.suptitle(
    "FOREARM sEMG MONITORING SYSTEM",
    fontsize=16,
    fontweight="bold"
)

line, = ax.plot(range(WINDOW_SIZE), list(signal), linewidth=1.3)
ax.set_title("Live Muscle Electrical Activity")
ax.set_xlabel("Recent Samples")
ax.set_ylabel("ADC Value")
ax.set_xlim(0, WINDOW_SIZE - 1)
ax.set_ylim(0, 1023)
ax.grid(True, alpha=0.3)

rms_text = fig.text(
    0.12, 0.91, "RMS: 0.00",
    fontsize=13, fontweight="bold"
)
activity_text = fig.text(
    0.43, 0.91, "ACTIVITY: LOW",
    fontsize=13, fontweight="bold"
)
record_text = fig.text(
    0.73, 0.91, "RECORDING: OFF",
    fontsize=11
)
connection_text = fig.text(
    0.12, 0.08, f"Connected: {PORT} | {BAUD_RATE} baud",
    fontsize=10
)

# ---------- BUTTONS ----------
start_ax = plt.axes([0.12, 0.13, 0.20, 0.07])
stop_ax = plt.axes([0.38, 0.13, 0.20, 0.07])
save_ax = plt.axes([0.64, 0.13, 0.20, 0.07])

start_button = Button(start_ax, "Start Recording")
stop_button = Button(stop_ax, "Stop Recording")
save_button = Button(save_ax, "Save CSV")


def start_recording(event):
    global recording, recording_start, sample_count

    if recording:
        return

    recorded_rows.clear()
    sample_count = 0
    recording_start = time.monotonic()
    recording = True
    record_text.set_text("RECORDING: ON")
    print("Recording started.")


def stop_recording(event):
    global recording

    recording = False
    record_text.set_text("RECORDING: OFF")
    print(f"Recording stopped. Samples: {len(recorded_rows)}")


def save_csv(event):
    if not recorded_rows:
        root = Tk()
        root.withdraw()
        messagebox.showinfo(
            "No data",
            "Start recording first, then collect some samples."
        )
        root.destroy()
        return

    root = Tk()
    root.withdraw()

    filename = filedialog.asksaveasfilename(
        parent=root,
        title="Save sEMG recording",
        defaultextension=".csv",
        initialfile="semg_recording.csv",
        filetypes=[("CSV files", "*.csv")]
    )

    if filename:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Sample",
                "Timestamp",
                "Elapsed_ms",
                "ADC_Value",
                "Window_RMS",
                "Activity_Status"
            ])
            writer.writerows(recorded_rows)

        messagebox.showinfo(
            "Saved",
            f"Saved {len(recorded_rows)} samples to:\n{filename}"
        )
        print(f"CSV saved: {filename}")

    root.destroy()


start_button.on_clicked(start_recording)
stop_button.on_clicked(stop_recording)
save_button.on_clicked(save_csv)


# ---------- LIVE UPDATE ----------
def update(frame):
    global current_rms, current_status, sample_count

    # Read available serial bytes without waiting for a full batch
    waiting = ser.in_waiting
    if waiting:
        byte_buffer.extend(ser.read(waiting))

    while b"\n" in byte_buffer:
        raw_line, _, remainder = byte_buffer.partition(b"\n")
        byte_buffer[:] = remainder

        try:
            value = int(raw_line.decode("utf-8").strip())
        except (ValueError, UnicodeDecodeError):
            continue

        if not 0 <= value <= 1023:
            continue

        signal.append(value)

        values = np.asarray(signal, dtype=float)
        centered = values - np.mean(values)
        current_rms = float(np.sqrt(np.mean(centered ** 2)))

        if current_rms >= THRESHOLD:
            current_status = "HIGH ACTIVITY"
        else:
            current_status = "LOW ACTIVITY"

        # Save each sample only while recording
        if recording:
            sample_count += 1
            elapsed_ms = (
                time.monotonic() - recording_start
            ) * 1000

            recorded_rows.append([
                sample_count,
                datetime.now().isoformat(timespec="milliseconds"),
                round(elapsed_ms, 2),
                value,
                round(current_rms, 3),
                current_status
            ])

    # Refresh dashboard
    line.set_ydata(list(signal))
    rms_text.set_text(f"RMS: {current_rms:.2f} ADC counts")
    activity_text.set_text(f"ACTIVITY: {current_status}")
    record_text.set_text(
        f"RECORDING: {'ON' if recording else 'OFF'}"
        f" | Samples: {len(recorded_rows)}"
    )

    return line, rms_text, activity_text, record_text


def close_dashboard(event):
    if ser.is_open:
        ser.close()


fig.canvas.mpl_connect("close_event", close_dashboard)

animation = FuncAnimation(
    fig,
    update,
    interval=UPDATE_INTERVAL,
    blit=False,
    cache_frame_data=False
)

try:
    plt.show()
finally:
    if ser.is_open:
        ser.close()

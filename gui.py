import tkinter as tk
from tkinter import ttk, filedialog
import requests
import pandas as pd
import threading
import os
import time

# Define separate API URLs for each Raspberry Pi
API_URLS = {
    'sensor1': 'http://10.19.142.230:5000/sensor_data',
    'sensor2': 'http://10.19.142.230:5000/sensor_data',
    'sensor3': 'http://10.19.142.230:5000/sensor_data'
}

# Data structures for each sensor
data = {
    'sensor1': {
        'timestamp': [],
        'lux': [],
        'visible': [],
        'infrared': [],
        'full_spectrum': [],
        'temperature': [],
        'humidity': [],
        'pressure': [],
        'sound_level': []
    },
    'sensor2': {
        'timestamp': [],
        'lux': [],
        'visible': [],
        'infrared': [],
        'full_spectrum': [],
        'temperature': [],
        'humidity': [],
        'pressure': [],
        'sound_level': []
    },
    'sensor3': {
        'timestamp': [],
        'lux': [],
        'visible': [],
        'infrared': [],
        'full_spectrum': [],
        'temperature': [],
        'humidity': [],
        'pressure': [],
        'sound_level': []
    }
}

class SensorDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sensor Data Monitor")

        # Create a frame for inputs
        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # File location input
        ttk.Label(frame, text="File location: ").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.file_location_var = tk.StringVar()
        self.file_location_entry = ttk.Entry(frame, textvariable=self.file_location_var, width=40)
        self.file_location_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Browse", command=self.browse_folder).grid(row=0, column=2, padx=5, pady=5)

        # Start and Stop buttons
        self.start_button = ttk.Button(frame, text="Start Recording", command=self.start_recording)
        self.start_button.grid(row=2, column=0, padx=5, pady=5)
        self.stop_button = ttk.Button(frame, text="Stop and Save", command=self.stop_and_save, state=tk.DISABLED)
        self.stop_button.grid(row=2, column=1, padx=5, pady=5)

        self.recording = False
        self.threads = []

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.file_location_var.set(folder_path)

    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Start a thread for each sensor
        for sensor in API_URLS.keys():
            thread = threading.Thread(target=self.record_data, args=(sensor,))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def stop_and_save(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # Wait for all threads to finish
        for thread in self.threads:
            thread.join()

        self.save_data()

    def record_data(self, sensor):
        while self.recording:
            try:
                response = requests.get(API_URLS[sensor])
                response.raise_for_status()
                sensor_data = response.json()
                now = time.localtime()
                timestamp = time.strftime('%m%d%y%H%M%S', now)  # Format as MMDDYYHHMMSS        
                data[sensor]['timestamp'].append(str(timestamp))
                data[sensor]['lux'].append(sensor_data['lux'])
                data[sensor]['visible'].append(sensor_data['visible'])
                data[sensor]['infrared'].append(sensor_data['infrared'])
                data[sensor]['full_spectrum'].append(sensor_data['full_spectrum'])
                data[sensor]['temperature'].append(sensor_data['temperature'])
                data[sensor]['humidity'].append(sensor_data['humidity'])
                data[sensor]['pressure'].append(sensor_data['pressure'])
                data[sensor]['sound_level'].append(sensor_data['sound_level'])
            except requests.RequestException as e:
                print(f"Error fetching data from {sensor}: {e}")
            time.sleep(2)  # Request data every 2 seconds

    def save_data(self):
        folder_path = self.file_location_var.get()
        if not folder_path:
            print("File location is not specified.")
            return

        for sensor, sensor_data in data.items():
            file_name = f"{sensor}_{time.strftime('%m%d%y%H%M%S')}.csv"
            file_path = os.path.join(folder_path, file_name)

            df = pd.DataFrame(sensor_data)
            df['timestamp'] = df['timestamp'].astype(str)
            df.to_csv(file_path, index=False)
            print(f"Data saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SensorDataApp(root)
    root.mainloop()

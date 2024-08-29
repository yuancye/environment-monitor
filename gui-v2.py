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
    'sensor2': 'http://10.19.142.231:5000/sensor_data',
    'sensor3': 'http://10.19.142.232:5000/sensor_data'
}

class SensorDataApp:
    def __init__(self, root):
        self.root = root
        self.sensor_windows = {}
        self.threads = {}
        self.recording_flags = {}
        self.current_data = {}
        self.timestamps = {}

        self.initialize_interfaces()

        # If no sensor windows were created, close the application
        if not self.sensor_windows:
            print("No servers are running. Exiting application.")
            self.root.quit()

    def initialize_interfaces(self):
        for sensor in API_URLS.keys():
            if self.check_server_status(sensor):
                self.create_sensor_window(sensor)

    def check_server_status(self, sensor):
        try:
            response = requests.get(API_URLS[sensor], timeout=5)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            return False

    def create_sensor_window(self, sensor):

        sensor_window = tk.Toplevel(self.root)
        sensor_window.title(f"{sensor.capitalize()} Data Monitor")
        sensor_frame = ttk.Frame(sensor_window, padding="10")
        sensor_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure rows and columns to be resizable
        sensor_window.columnconfigure(0, weight=1)
        sensor_window.rowconfigure(0, weight=1)
        sensor_frame.columnconfigure(0, weight=1)
        sensor_frame.columnconfigure(1, weight=3)  # Entry field should take more space
        sensor_frame.columnconfigure(2, weight=1)
        sensor_frame.rowconfigure(0, weight=1)
        sensor_frame.rowconfigure(1, weight=1)

        # File location input for each sensor
        ttk.Label(sensor_frame, text="File location: ").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        file_location_var = tk.StringVar()
        file_location_entry = ttk.Entry(sensor_frame, textvariable=file_location_var)
        file_location_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        ttk.Button(sensor_frame, text="Browse", command=lambda: self.browse_folder(file_location_var)).grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Start and Stop buttons for each sensor
        start_button = ttk.Button(sensor_frame, text="Start Recording", command=lambda: self.start_recording(sensor, file_location_var, start_button, stop_button))
        start_button.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        stop_button = ttk.Button(sensor_frame, text="Stop and Save", command=lambda: self.stop_and_save(sensor, start_button, stop_button), state=tk.DISABLED)
        stop_button.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        # Store references to the window elements
        self.sensor_windows[sensor] = {
            'window': sensor_window,
            'file_location_var': file_location_var,
            'start_button': start_button,
            'stop_button': stop_button
        }

        # Initialize data and flags
        self.current_data[sensor] = {}
        self.recording_flags[sensor] = False
        self.threads[sensor] = None
        self.timestamps[sensor] = None

    def browse_folder(self, file_location_var):
        folder_path = filedialog.askdirectory()
        if folder_path:
            file_location_var.set(folder_path)

    def start_recording(self, sensor, file_location_var, start_button, stop_button):
        self.recording_flags[sensor] = True
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

        # Clear previous data and set a new timestamp
        self.current_data[sensor] = {
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
        self.timestamps[sensor] = time.strftime('%m%d%y%H%M%S')

        # Start a new thread for the sensor recording
        thread = threading.Thread(target=self.record_data, args=(sensor,))
        thread.daemon = True
        thread.start()
        self.threads[sensor] = thread

    def stop_and_save(self, sensor, start_button, stop_button):
        self.recording_flags[sensor] = False
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

        # Wait for the thread to finish
        if self.threads[sensor] is not None:
            self.threads[sensor].join()

        self.save_data(sensor)

    def record_data(self, sensor):
        while self.recording_flags[sensor]:
            try:
                response = requests.get(API_URLS[sensor])
                response.raise_for_status()
                sensor_data = response.json()
                now = time.localtime()
                timestamp = time.strftime('%m%d%y%H%M%S', now)  # Format as MMDDYYHHMMSS        
                self.current_data[sensor]['timestamp'].append(str(timestamp))
                self.current_data[sensor]['lux'].append(sensor_data['lux'])
                self.current_data[sensor]['visible'].append(sensor_data['visible'])
                self.current_data[sensor]['infrared'].append(sensor_data['infrared'])
                self.current_data[sensor]['full_spectrum'].append(sensor_data['full_spectrum'])
                self.current_data[sensor]['temperature'].append(sensor_data['temperature'])
                self.current_data[sensor]['humidity'].append(sensor_data['humidity'])
                self.current_data[sensor]['pressure'].append(sensor_data['pressure'])
                self.current_data[sensor]['sound_level'].append(sensor_data['sound_level'])
            except requests.RequestException as e:
                print(f"Error fetching data from {sensor}: {e}")
            time.sleep(2)  # Request data every 2 seconds

    def save_data(self, sensor):
        folder_path = self.sensor_windows[sensor]['file_location_var'].get()
        if not folder_path:
            print(f"File location for {sensor} is not specified.")
            return

        file_name = f"{sensor}_{self.timestamps[sensor]}.csv"
        file_path = os.path.join(folder_path, file_name)

        df = pd.DataFrame(self.current_data[sensor])
        df['timestamp'] = df['timestamp'].astype(str)
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Hide the root window
    root.withdraw()
    
    app = SensorDataApp(root)
    root.mainloop()

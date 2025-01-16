import os
import time
import logging
import pygetwindow as gw
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

# ---------------------------
# Detailed File Event Handler
# ---------------------------

class FileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        log_event(f'File modified: {event.src_path}')
    
    def on_deleted(self, event):
        log_event(f'File deleted: {event.src_path}')
    
    def on_created(self, event):
        log_event(f'File created: {event.src_path}')
    
    def on_moved(self, event):
        log_event(f'File moved: {event.src_path} -> {event.dest_path}')
    
    def on_renamed(self, event):
        log_event(f'File renamed: {event.src_path} -> {event.dest_path}')

# ----------------------
# Logging Events to Date-based Folder
# ----------------------

def log_event(event_message):
    # Get the current date to create folders for year, month, and day
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day

    # Create the folder structure
    log_dir = os.path.join("logs", str(year), f"{month:02d}", f"{day:02d}")
    os.makedirs(log_dir, exist_ok=True)

    # Define the log file path
    log_file = os.path.join(log_dir, "file_events.log")

    # Configure logging to append to the correct log file
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    # Log the event
    logging.info(event_message)

# ------------------------
# Track Active Window
# ------------------------

def track_active_window():
    last_window = None
    while True:
        active_window = gw.getActiveWindow()
        if active_window:
            # Only log if the active window has changed
            if active_window.title != last_window:
                log_event(f"Active window: {active_window.title}")
                last_window = active_window.title
        time.sleep(1)

# ----------------------------
# System Tray Application
# ----------------------------

def create_system_tray_icon():
    icon_image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(icon_image)
    draw.text((10, 10), "Tracking", fill=(0, 0, 0))

    def quit_action(icon, item):
        icon.stop()

    menu = Menu(MenuItem('Quit', quit_action))

    icon = Icon("Window File Tracker", icon_image, menu=menu)
    icon.run()

# ------------------------------
# File Viewer GUI
# ------------------------------

class EventDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Tracker")
        
        # Set window size to 80% of screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.8)  # 80% of the screen width
        window_height = int(screen_height * 0.8)  # 80% of the screen height
        self.root.geometry(f"{window_width}x{window_height}")

        # Text box to display events
        self.textbox = tk.Text(root, width=150, height=40)
        self.textbox.pack()

        # Button to refresh the log
        self.refresh_button = tk.Button(root, text="Refresh Log", command=self.refresh_log)
        self.refresh_button.pack()

        # Button to open file viewer
        self.view_file_button = tk.Button(root, text="View Last Edited File", command=self.view_file)
        self.view_file_button.pack()

        # Button to select log folder
        self.select_folder_button = tk.Button(root, text="Select Log Folder", command=self.select_log_folder)
        self.select_folder_button.pack()

        self.refresh_log()

    def refresh_log(self):
        self.textbox.delete(1.0, tk.END)  # Clear the text box

        # Get the current date to construct the log file path
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month
        day = current_date.day

        # Build the log file path based on the partitioned folder structure
        log_dir = os.path.join("logs", str(year), f"{month:02d}", f"{day:02d}")
        log_file = os.path.join(log_dir, "file_events.log")

        # Ensure the log file exists, if not, create it
        if not os.path.exists(log_file):
            with open(log_file, 'w'):  # Just create the file if it doesn't exist
                pass

        # Read the log content from the file
        with open(log_file, "r") as file:
            log_content = file.readlines()  # Read all lines from the log file
            log_content.reverse()  # Reverse the list of log entries to display them in descending order
            self.textbox.insert(tk.END, ''.join(log_content))  # Insert the reversed log content

    def view_file(self):
        # Prompt the user to select a file to view its content
        file_path = filedialog.askopenfilename(title="Open File")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.show_file_content(content)
            except Exception as e:
                print(f"Error reading file: {e}")

    def show_file_content(self, content):
        file_window = tk.Toplevel(self.root)
        file_window.title("File Content")

        textbox = tk.Text(file_window, width=80, height=20)
        textbox.pack()
        textbox.insert(tk.END, content)

    def select_log_folder(self):
        folder_path = filedialog.askdirectory(title="Select Log Folder")
        if folder_path:
            self.load_logs_from_folder(folder_path)

    def load_logs_from_folder(self, folder_path):
        self.textbox.delete(1.0, tk.END)  # Clear the text box
        logs_found = False  # Track if any logs were found

        # Check if the folder contains a file named 'file_events.log'
        log_file_path = os.path.join(folder_path, "file_events.log")

        # If the log file exists, read and display it
        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as log_file:
                log_content = log_file.readlines()
                log_content.reverse()  # Reverse to display in descending order
                self.textbox.insert(tk.END, ''.join(log_content))
                logs_found = True  # Mark that logs were found

        # If no log file is found, show a message in the text box
        if not logs_found:
            self.textbox.insert(tk.END, "No logs found for the selected date.\n")

# ----------------------
# Main Function
# ----------------------

def start_file_tracking(path_to_monitor):
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_monitor, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def run_gui():
    root = tk.Tk()
    EventDisplayApp(root)
    root.mainloop()

if __name__ == "__main__":
    # Start the window and file tracking
    path_to_monitor = 'C:/Nijat/3.Documents'  # Adjust the path to your needs
    # Run file tracking in a separate thread
    import threading
    threading.Thread(target=start_file_tracking, args=(path_to_monitor,), daemon=True).start()

    # Start tracking active window
    threading.Thread(target=track_active_window, daemon=True).start()

    # Run the system tray application
    threading.Thread(target=create_system_tray_icon, daemon=True).start()

    # Run the GUI
    run_gui()

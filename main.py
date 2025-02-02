import os
import time
import logging
import threading
# import secrets
import random
import string
import pyperclip
import pygetwindow as gw
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from datetime import datetime, timedelta
import hashlib

RESET_CODE_FILE = "reset_code.txt"
CONFIG_FILE = "config.txt"
DEFAULT_PATH = "C:/Users/Public"

# ---------------------------
# Utility Functions
# ---------------------------

def generate_reset_code_with_length(length=5):
    """Generate a reset code with the specified length."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_credentials(username, password):
    credentials_dir = "credentials"
    os.makedirs(credentials_dir, exist_ok=True)
    with open(os.path.join(credentials_dir, "user_credentials.txt"), "w") as f:
        f.write(f"{username}\n{hash_password(password)}")

def load_credentials():
    try:
        credentials_dir = "credentials"
        with open(os.path.join(credentials_dir, "user_credentials.txt"), "r") as f:
            data = f.readlines()
            return data[0].strip(), data[1].strip()
    except FileNotFoundError:
        return None, None

def generate_reset_code(username):
    # reset_code = secrets.token_hex(8)  # Generate secure random reset code
    reset_code = generate_reset_code_with_length(5)  # Generate a 5-character reset code
    pyperclip.copy(reset_code)  # Copy reset code to clipboard
    expiration_time = datetime.now() + timedelta(minutes=30)  # Code valid for 30 minutes
    with open(RESET_CODE_FILE, "w") as file:
        file.write(f"{username}|{reset_code}|{expiration_time.isoformat()}")
    messagebox.showinfo("Reset Code", f"A reset code has been generated: {reset_code}\n\nThe code has been copied to your clipboard.")
    
def verify_reset_code(username, input_code):
    if not os.path.exists(RESET_CODE_FILE):
        return False, "Reset code not found. Request a new one."
    
    with open(RESET_CODE_FILE, "r") as file:
        data = file.read().strip()
        stored_username, stored_code, expiration_time = data.split("|")
    
    if username != stored_username:
        return False, "Invalid username."
    
    if input_code != stored_code:
        return False, "Invalid reset code."
    
    if datetime.now() > datetime.fromisoformat(expiration_time):
        return False, "Reset code expired."
    
    return True, "Reset code verified."

def reset_password(username, new_password, root):
    # new_password = simpledialog.askstring("Reset Password", "Enter a new password:", show="*")
    is_valid, message = verify_reset_code(username, input_code=simpledialog.askstring("Reset code", "Enter reset code: ", show="*"))
    if not is_valid:
        messagebox.showerror("Error", message)
        return
    
    # Update password securely (hash and store it)
    save_credentials(username, new_password)
    messagebox.showinfo("Success", "Password reset successful!")
    root.destroy()

def load_folder_path():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config_data = file.read().strip()
            if config_data:
                return config_data
            else:
                save_folder_path(DEFAULT_PATH)
                return DEFAULT_PATH
    else:
        # Create a config file with the default path
        save_folder_path(DEFAULT_PATH)
        return DEFAULT_PATH

def save_folder_path(path):
    with open(CONFIG_FILE, "w") as file:
        file.write(path)

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

def open_main_app(root):
    root.destroy()
    main_root = tk.Tk()
    EventDisplayApp(main_root)
    main_root.mainloop()

# ---------------------------
# Login Screen
# ---------------------------

def setup_login(root):
    root.title("Login Screen")
    root.geometry("400x300")  # Set the size of the window
    root.resizable(False, False)  # Disable resizing

    # Load credentials from storage
    username, password_hash = load_credentials()

    # First-Time Setup
    if not username:
        frame = tk.Frame(root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Setup Your Account", font=("Arial", 16)).pack(pady=(0, 10))
        
        tk.Label(frame, text="Set a Username:").pack(anchor="w")
        username_entry = tk.Entry(frame, width=30)
        username_entry.pack(pady=5)

        tk.Label(frame, text="Set a Password:").pack(anchor="w")
        password_entry = tk.Entry(frame, show='*', width=30)
        password_entry.pack(pady=5)

        def save_setup():
            username_input = username_entry.get().strip()
            password_input = password_entry.get().strip()

            if not username_input:
                messagebox.showerror("Error", "Username is required.")
                return

            if not password_input:
                messagebox.showerror("Error", "Password is required.")
                return

            save_credentials(username_input, password_input)
            messagebox.showinfo("Success", "Setup completed. Restart the application.")
            root.destroy()

        tk.Button(frame, text="Save", command=save_setup, width=20).pack(pady=10)
        return  # Exit setup method after first-time setup

    # Login Screen
    else:
        frame = tk.Frame(root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Login", font=("Arial", 16)).pack(pady=(0, 10))
        
        tk.Label(frame, text="Enter Username:").pack(anchor="w")
        username_entry = tk.Entry(frame, width=30)
        username_entry.pack(pady=5)

        tk.Label(frame, text="Enter Password:").pack(anchor="w")
        password_entry = tk.Entry(frame, show='*', width=30)
        password_entry.pack(pady=5)

        attempts = [0]  # Using a list to mutate attempts within inner functions

        def attempt_login():
            if attempts[0] >= 3:
                messagebox.showerror("Error", "Maximum attempts reached.")
                root.destroy()
                return
            
            username_input = username_entry.get().strip()
            password_input = password_entry.get().strip()

            if username_input == username and hash_password(password_input) == password_hash:
                messagebox.showinfo("Success", "Login successful.")
                open_main_app(root)  # Open the main app after successful login
            else:
                attempts[0] += 1
                remaining_attempts = 3 - attempts[0]
                messagebox.showerror("Error", f"Invalid credentials. {remaining_attempts} attempt(s) remaining.")

        def reset_attempt():
            ask_username = simpledialog.askstring("Reset Password", "Enter username:")
            if ask_username != username:
                messagebox.showerror("Error", "Invalid username.")
                return
            
            generate_reset_code(username)
            messagebox.showinfo("Reset Code", "A reset code has been generated. Use it to reset your password.")
            
            new_password = simpledialog.askstring("Reset Password", "Enter a new password:", show="*")
            if not new_password:
                messagebox.showerror("Error", "Password is required to reset.")
                return
            if reset_password(username, new_password, root):
                messagebox.showinfo("Success", "Password reset successful.")
                root.destroy()

        tk.Button(frame, text="Login", command=attempt_login, width=20).pack(pady=10)
        tk.Button(frame, text="Forgot Password?", command=reset_attempt, width=20).pack(pady=5)
        
        root.mainloop()
        return
    
# ---------------------------
# File Event Handler
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
# Logging Events
# ----------------------

def log_event(event_message):
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day

    log_dir = os.path.join("logs", str(year), f"{month:02d}", f"{day:02d}")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "file_events.log")
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
    logging.info(event_message)

# ------------------------
# Track Active Window
# ------------------------

def track_active_window():
    last_window = None
    while True:
        active_window = gw.getActiveWindow()
        if active_window:
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
        self.root.title("Event Tracker by Nijat Aliyev (@developer.nijat)")

        # Set window size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.minsize(800, 600)

        # Main frame
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Textbox for log display
        self.textbox = tk.Text(
            main_frame,
            wrap=tk.WORD,
            font=("Courier", 12),
            bg="#f5f5f5",
            fg="#333",
            relief=tk.SUNKEN,
            bd=2
        )
        self.textbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        self.refresh_button = tk.Button(
            button_frame, text="Refresh Log", command=self.refresh_log, width=20, bg="#757373", fg="white", font=("Arial", 10, "bold")
        )
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.view_file_button = tk.Button(
            button_frame, text="View Last Edited File", command=self.view_file, width=20, bg="#757373", fg="white", font=("Arial", 10, "bold")
        )
        self.view_file_button.pack(side=tk.LEFT, padx=5)

        self.select_folder_button = tk.Button(
            button_frame, text="Select Log Folder", command=self.select_log_folder, width=20, bg="#757373", fg="white", font=("Arial", 10, "bold")
        )
        self.select_folder_button.pack(side=tk.LEFT, padx=5)
        
        self.select_folder_tracking_button = tk.Button(
            button_frame, text="Setup Tracking Folder", command=self.select_tracking_folder, width=20, bg="#757373", fg="white", font=("Arial", 10, "bold")
        )
        self.select_folder_tracking_button.pack(side=tk.LEFT, padx=5)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor="w", bg="#ddd", fg="#555")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Initial load
        self.refresh_log()

    def set_status(self, message):
        self.status_var.set(message)

    def refresh_log(self):
        self.textbox.delete(1.0, tk.END)
        current_date = datetime.now()
        year = current_date.year
        month = current_date.month
        day = current_date.day

        log_dir = os.path.join("logs", str(year), f"{month:02d}", f"{day:02d}")
        log_file = os.path.join(log_dir, "file_events.log")

        if not os.path.exists(log_file):
            with open(log_file, 'w'):
                pass

        with open(log_file, "r") as file:
            log_content = file.readlines()
            log_content.reverse()
            self.textbox.insert(tk.END, ''.join(log_content))

        self.set_status(f"Logs refreshed from: {log_file}")

    def view_file(self):
        file_path = filedialog.askopenfilename(title="Open File")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    self.show_file_content(content)
                self.set_status(f"Opened file: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")

    def show_file_content(self, content):
        file_window = tk.Toplevel(self.root)
        file_window.title("File Content")
        file_window.geometry("600x400")

        textbox = tk.Text(file_window, wrap=tk.WORD, font=("Courier", 11), bg="#f9f9f9", fg="#333")
        textbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        textbox.insert(tk.END, content)

    def select_log_folder(self):
        folder_path = filedialog.askdirectory(title="Select Log Folder")
        if folder_path:
            self.load_logs_from_folder(folder_path)

    def select_tracking_folder(self):
        folder = filedialog.askdirectory(title="Select Folder to Monitor")
        if folder:
            current_path_var = tk.StringVar(value=load_folder_path())
            current_path_var.set(folder)
            save_folder_path(folder)
            threading.Thread(target=start_file_tracking, args=(folder,), daemon=True).start()
            messagebox.showinfo("Monitoring Folder Updated", f"Monitoring folder set to: {folder}")
            return folder
        else:
            messagebox.showwarning("No Folder Selected", "Please select a folder to monitor.")
            return None
    
    def load_logs_from_folder(self, folder_path):
        self.textbox.delete(1.0, tk.END)
        logs_found = False

        log_file_path = os.path.join(folder_path, "file_events.log")

        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as log_file:
                log_content = log_file.readlines()
                log_content.reverse()
                self.textbox.insert(tk.END, ''.join(log_content))
                logs_found = True

        if not logs_found:
            self.textbox.insert(tk.END, "No logs found for the selected folder.\n")

        self.set_status(f"Logs loaded from: {folder_path}")

# ----------------------
# Main Functions
# ----------------------

def run_gui():
    root = tk.Tk()

    if not setup_login(root):
        return

if __name__ == "__main__":
    path_to_monitor = load_folder_path()
    
    threading.Thread(target=start_file_tracking, args=(path_to_monitor,), daemon=True).start()
    threading.Thread(target=track_active_window, daemon=True).start()
    threading.Thread(target=create_system_tray_icon, daemon=True).start()
    run_gui()

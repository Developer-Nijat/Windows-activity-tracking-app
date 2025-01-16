# Windows Activity Tracking Application

This application is designed to track and log file system changes, active window titles, and provide user-friendly account authentication with password management. It features a robust GUI built with **Tkinter** and integrates system-level monitoring with file and window event tracking.

### Features

1. **Account Setup and Login**:
   - First-time user account setup with username and password.
   - Secure password storage with SHA-256 hashing.
   - Login system with validation and error handling for failed attempts.

2. **Password Reset**:
   - Generates a reset code for forgotten passwords.
   - Securely resets and updates passwords with validation.

3. **File System Event Tracker**:
   - Monitors file modifications, deletions, creations, and movements.
   - Logs events into categorized folders based on date.

4. **Active Window Tracker**:
   - Tracks active window titles and logs transitions.
   - Useful for productivity analysis and auditing.

5. **Graphical User Interface (GUI)**:
   - Intuitive interface for managing credentials and viewing logs.
   - Displays tracked events in a user-friendly text display area.
   - Allows users to refresh logs or view specific files.

6. **System Tray Integration**:
   - Minimal system tray app for monitoring and quick access.
   - Includes options for quitting the application.

7. **Customization Options**:
   - Set log directories and manage log files.
   - Easily select and view logs from a specific folder.

### Technical Details

- **Python Libraries Used**:
  - `Tkinter`: For GUI development.
  - `watchdog`: For monitoring file system changes.
  - `pygetwindow`: To track active windows.
  - `pystray`: For creating a system tray application.
  - `logging`: For structured and organized logging of events.
  - `pyperclip`: For clipboard integration (e.g., copying reset codes).
  - `hashlib`: For secure password hashing.

- **Directory Structure**:
  - Logs are stored in a hierarchical format by year, month, and day.
  - Credentials are stored securely in a dedicated folder.

### How to Use

1. **Setup**:
   - On the first run, set up a username and password.
   - Restart the application after setup.

2. **Login**:
   - Enter your username and password to access the main event tracker.

3. **Track Events**:
   - File system changes and active windows are automatically logged.

4. **View Logs**:
   - Use the GUI to refresh and view the latest logs.
   - Optionally, navigate to specific log files.

5. **Reset Password**:
   - Use the "Forgot Password?" option to generate and verify a reset code.
   - Update your password securely.

6. **System Tray**:
   - Minimize the application and access it through the system tray icon.

### Future Enhancements
- Add email integration for password reset notifications.
- Introduce dark mode for improved accessibility.
- Provide options for exporting logs as CSV or PDF reports.

### Author
**Nijat Aliyev**  

GitHub: [@Developer-Nijat](https://github.com/Developer-Nijat) 

Website: [aliyev.dev](https://aliyev.dev)

YouTube: [@developer_nijat](https://www.youtube.com/@developer_nijat)


---

### Step 5: Set Up the Project

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Developer-Nijat/Windows-activity-tracking-app
   cd Windows-activity-tracking-app
   ```

2. **Create a Virtual Environment**:
   Create and activate a virtual environment:
   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   Install the libraries from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the App**:
   Run the Python app:
   ```bash
   python main.py
   ```

---

### What Happens When Pulling the Project?

- The `venv` folder and `logs` directory won't be included (excluded by `.gitignore`).
- When pulling the project to another computer, you'll need to set up the virtual environment and install the dependencies using `requirements.txt`.

This setup ensures that your project remains lightweight and portable, and anyone (including you) can easily set it up on another machine. Let me know if you need help with any of these steps!
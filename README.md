### Windows Activity Tracking Application

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
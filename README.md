# Personal Security Operations Center (SOC) Dashboard

## Overview
This project is a comprehensive, personal Security Operations Center (SOC) dashboard that provides a unified view of various security events. It integrates multiple monitoring components, including a honeypot and log analysis, into a single, interactive web interface. This system is designed to simulate a professional-grade security tool, demonstrating advanced skills in software architecture, network security, and data visualization.

---

## Architecture
The system is built on a modular architecture:
- **Backend (`app.py`):** A Flask web server that serves the frontend and provides API endpoints for data retrieval.
- **Monitoring Engine (`monitor.py`):** A separate, persistent script that runs background security tasks like the honeypot. It writes all findings to a central database.
- **Database (`database.py` & `soc_database.db`):** An SQLite database that acts as the central repository for all alerts and events, decoupling the monitoring engine from the web server.
- **Frontend (`index.html`):** A dynamic, single-page dashboard that fetches data from the backend APIs and displays it in real-time.

---

## Features
- **Live Alert Feed:** Displays security alerts from all monitoring sources in real-time.
- **Honeypot Integration:** A simple TCP honeypot runs in the background, logging all connection attempts as high-severity alerts.
- **Dynamic Dashboard:** The web interface automatically refreshes every 5 seconds to show the latest data.
- **Data Visualization:** Includes a doughnut chart (via Chart.js) to visualize the distribution of alert types.
- **Centralized Database:** All events are stored in an SQLite database for persistence and analysis.
- **Modular and Scalable:** The architecture is designed to be easily extensible with new monitoring modules (e.g., log file analysis, network scanning, threat intelligence lookups).

---

## Technologies Used
- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Data Visualization:** Chart.js
- **Database:** SQLite
- **Networking:** `socket` library
- **(Optional) Packet Manipulation:** `scapy` (for future network scanning features)

---

## Setup and Usage

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/Personal-SOC-Dashboard.git](https://github.com/YourUsername/Personal-SOC-Dashboard.git)
cd Personal-SOC-Dashboard
```

### 2. Create Directory Structure
Ensure you have the `templates` and `static/js` subdirectories.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the System
This system requires two separate processes to run concurrently. Open two terminals.

**In Terminal 1 - Start the Monitoring Engine:**
This script will run continuously to listen for security events.
```bash
python monitor.py
```

**In Terminal 2 - Start the Flask Web Server:**
This serves the dashboard to your browser.
```bash
python app.py
```

### 5. Access the Dashboard
Open your web browser and navigate to:
**`http://127.0.0.1:5000`**

You should now see the SOC dashboard. To generate an alert, you can try connecting to the honeypot from a third terminal:
```bash
telnet 127.0.0.1 2323
```
Within a few seconds, you should see a "Honeypot Connection" alert appear on the dashboard.

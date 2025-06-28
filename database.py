import sqlite3
from datetime import datetime

DATABASE_NAME = 'soc_database.db'

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    cursor = conn.cursor()
    
    # Create alerts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            alert_type TEXT NOT NULL,
            description TEXT NOT NULL,
            source_ip TEXT,
            severity TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("[INFO] Database initialized successfully.")

def add_alert(alert_type, description, source_ip=None, severity='Medium'):
    """Adds a new alert to the database."""
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    cursor = conn.cursor()
    timestamp = datetime.now()
    cursor.execute('''
        INSERT INTO alerts (timestamp, alert_type, description, source_ip, severity)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, alert_type, description, source_ip, severity))
    conn.commit()
    conn.close()

def get_recent_alerts(limit=50):
    """Fetches the most recent alerts from the database."""
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row # To access columns by name
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?', (limit,))
    alerts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return alerts

def get_alert_stats():
    """Gets statistics about alert types."""
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT alert_type, COUNT(*) as count FROM alerts GROUP BY alert_type')
    stats = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return stats

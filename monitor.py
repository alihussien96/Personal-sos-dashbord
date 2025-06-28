# This is the background monitoring engine.
# In a real-world scenario, each function would run in a separate thread.
import socket
import database
import time
import configparser

def start_honeypot():
    """A simple honeypot to capture connection attempts."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    host = '0.0.0.0'
    port = int(config['honeypot']['port'])
    
    print(f"[*] Honeypot starting on port {port}")
    database.init_db() # Ensure DB is ready

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                source_ip, source_port = addr
                description = f"Connection attempt from {source_ip}:{source_port} to honeypot port {port}."
                print(f"[ALERT] {description}")
                database.add_alert(
                    alert_type='Honeypot Connection', 
                    description=description, 
                    source_ip=source_ip, 
                    severity='High'
                )
                try:
                    conn.sendall(b'ACCESS DENIED.\n')
                except socket.error:
                    pass

def main():
    print("[MONITOR] Starting monitoring services...")
    # For this project, we are only starting the honeypot.
    # Other monitors (log file, network scan) can be added here as separate threads.
    start_honeypot()

if __name__ == '__main__':
    main()

from flask import Flask, render_template, jsonify, request
import database
import configparser
import requests # Make sure you have 'requests' in your requirements.txt

app = Flask(__name__)

# Function to query VirusTotal (simplified version)
def query_virustotal(ip_address):
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['virustotal'].get('api_key')

    if not api_key or 'YOUR_API_KEY' in api_key:
        return {"error": "VirusTotal API key not configured."}

    url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip_address}'
    headers = {'x-apikey': api_key}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        attributes = response.json().get('data', {}).get('attributes', {})
        stats = attributes.get('last_analysis_stats', {})
        return {
            "owner": attributes.get('as_owner', 'N/A'),
            "country": attributes.get('country', 'N/A'),
            "malicious": stats.get('malicious', 0),
            "suspicious": stats.get('suspicious', 0)
        }
    except requests.exceptions.HTTPError as e:
        return {"error": f"API Error: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/alerts')
def api_alerts():
    alerts = database.get_recent_alerts()
    return jsonify(alerts)

@app.route('/api/alert_stats')
def api_alert_stats():
    stats = database.get_alert_stats()
    labels = [stat['alert_type'] for stat in stats]
    data = [stat['count'] for stat in stats]
    return jsonify({'labels': labels, 'data': data})

@app.route('/api/lookup', methods=['POST'])
def api_lookup():
    """API endpoint to handle IOC lookups."""
    data = request.get_json()
    ip_to_check = data.get('ip')

    if not ip_to_check:
        return jsonify({"error": "IP address is required."}), 400

    # For this example, we only query VirusTotal
    vt_results = query_virustotal(ip_to_check)
    
    # In a real app, you would query more sources here
    
    return jsonify({"virustotal": vt_results})


if __name__ == '__main__':
    database.init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
    

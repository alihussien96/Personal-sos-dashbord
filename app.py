from flask import Flask, render_template, jsonify, request
import database
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Renders the main dashboard page."""
    return render_template('index.html')

@app.route('/api/alerts')
def api_alerts():
    """API endpoint to get the latest alerts."""
    alerts = database.get_recent_alerts()
    return jsonify(alerts)

@app.route('/api/alert_stats')
def api_alert_stats():
    """API endpoint to get alert statistics for charts."""
    stats = database.get_alert_stats()
    # Format for Chart.js
    labels = [stat['alert_type'] for stat in stats]
    data = [stat['count'] for stat in stats]
    return jsonify({'labels': labels, 'data': data})

if __name__ == '__main__':
    database.init_db()
    # host='0.0.0.0' makes it accessible from other devices on the network
    app.run(host='0.0.0.0', port=5000, debug=False)

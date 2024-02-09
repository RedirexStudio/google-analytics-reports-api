from flask import Flask, jsonify
from api_requests.ga_requests import events_report

app = Flask(__name__)

@app.route('/')
def home():
    return 'GA4 API for CENTRIUM: Server started successfully.'

@app.route('/events-report')
def run_events_report():
    result = events_report()

    if 'error' in result:
        return jsonify({'error': result['error']}), 500

    return jsonify(result['report'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, request, jsonify
from api_requests.ga_requests import events_report
from features.validator import is_valid_date, is_valid_text, is_valid_bsc_address

app = Flask(__name__)

@app.route('/')
def home():
    return 'GA4 API for CENTRIUM: Server started successfully.'

@app.route('/events-report')
def run_events_report():
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    eventNameFilter = request.args.get('eventNameFilter')
    inviterParameterFilter = request.args.get('inviterFilter')

    if startDate:
        if not (is_valid_date(startDate)):
            raise ValueError("startDate is in invalid format")
    if endDate:
        if not (is_valid_date(endDate)):
            raise ValueError("endDate is in invalid format")
    if eventNameFilter:
        if not (is_valid_text(eventNameFilter)):
            raise ValueError("eventNameFilter is in invalid format")
    if inviterParameterFilter:
        if not (is_valid_bsc_address(inviterParameterFilter)):
            raise ValueError("inviterParameterFilter is in invalid format")
    
    result = events_report(startDate, endDate, eventNameFilter, inviterParameterFilter)

    if 'error' in result:
        return jsonify({'error': result['error']}), 500

    return jsonify(result['report'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
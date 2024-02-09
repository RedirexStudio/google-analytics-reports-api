import os
import json
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

def events_report():
    # credentials
    PROPERTY_ID = os.environ.get('GA_PROPERTY_ID')
    CREDENTIALS_JSON = os.environ.get('GA_CREDENTIALS_JSON')

    if not (PROPERTY_ID and CREDENTIALS_JSON):
        raise ValueError("GA_PROPERTY_ID and GA_CREDENTIALS_JSON must be set in the environment")

    client = BetaAnalyticsDataClient.from_service_account_json(CREDENTIALS_JSON)

    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name="city"), Dimension(name="eventName")],
        metrics=[Metric(name="activeUsers"), Metric(name="eventCount")],
        date_ranges=[DateRange(start_date="2020-03-31", end_date="today")],
    )

    try:
        # Execute the API request
        response = client.run_report(request)

        # Prepare the response data
        report_data = []
        for row in response.rows:
            report_data.append({
                'eventName': row.dimension_values[1].value,
                'eventCount': row.metric_values[1].value,
                'city': row.dimension_values[0].value,
                'activeUsers': row.metric_values[0].value
            })

        # Return a JSON response
        return {'report': report_data}

    except Exception as e:
        # Handle the exception or return an error response
        return {'error': str(e)}
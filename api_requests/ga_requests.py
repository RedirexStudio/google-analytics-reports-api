import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    FilterExpression,
    FilterExpressionList,
    Filter,
)

def events_report(startDate, endDate, eventNameFilter, inviterParameterFilter):
    # credentials
    PROPERTY_ID = os.environ.get('GA_PROPERTY_ID')
    CREDENTIALS_JSON = os.environ.get('GA_CREDENTIALS_JSON')

    if not (PROPERTY_ID and CREDENTIALS_JSON):
        raise ValueError("GA_PROPERTY_ID and GA_CREDENTIALS_JSON must be set in the environment")

    client = BetaAnalyticsDataClient.from_service_account_json(CREDENTIALS_JSON)

    # Add all filters if exists
    filter_expressions = [
        FilterExpression(
            filter=Filter(
                field_name="eventName",
                string_filter=Filter.StringFilter(
                    match_type=Filter.StringFilter.MatchType.CONTAINS,
                    value=eventNameFilter
                ),
            )
        ) if eventNameFilter else None,
        FilterExpression(
            filter=Filter(
                field_name="customEvent:inviter",
                string_filter=Filter.StringFilter(value=inviterParameterFilter)
            ),
        ) if inviterParameterFilter else None,
    ]

    # Remove any None values from the list (filters with no conditions)
    filter_expressions = [expr for expr in filter_expressions if expr is not None]

    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name="city"), Dimension(name="eventName"), Dimension(name="customEvent:address"), Dimension(name="customEvent:deposit"), Dimension(name="customEvent:inviter")],
        metrics=[Metric(name="activeUsers"), Metric(name="eventCount")],
        date_ranges=[DateRange(start_date=(startDate if startDate is not None else "2020-03-31"), end_date=(endDate if endDate is not None else "today"))],
        dimension_filter=FilterExpression(
            and_group=FilterExpressionList(
                expressions=filter_expressions
            )
        ) if filter_expressions else None
    )

    try:
        # Execute the API request
        response = client.run_report(request)

        # Prepare the response data
        report_data = []
        for row in response.rows:
            report_data.append({
                'eventName': row.dimension_values[1].value,
                'address': row.dimension_values[2].value,
                'depositAmount': row.dimension_values[3].value,
                'inviter': row.dimension_values[4].value,
                'eventCount': row.metric_values[1].value,
                'city': row.dimension_values[0].value,
                'activeUsers': row.metric_values[0].value
            })

        # Return a JSON response
        return {'report': report_data}

    except Exception as e:
        # Handle the exception or return an error response
        return {'error': str(e)}
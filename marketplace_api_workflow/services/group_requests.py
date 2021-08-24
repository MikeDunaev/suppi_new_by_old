import datetime, dateutil.relativedelta


def _adjust_requests() -> dict:
    """
    Формирует запросы по методам.
    Returns:
    Cловарь с двумя методами: daily, monthly.
    """
    today = str(datetime.date.today())
    six_days_ago = str(datetime.date.today() - datetime.timedelta(days=6))
    day_ago = str(datetime.date.today() - datetime.timedelta(days=1))
    seven_days_ago = str(datetime.date.today() - datetime.timedelta(days=7))
    thirteen_days_ago = str(datetime.date.today() - datetime.timedelta(days=13))
    month_ago = str(datetime.date.today() - dateutil.relativedelta.relativedelta(months=1))

    hours_methods = {
        # daily analytics data
        'v1_analytics_data_today': ("/v1/analytics/data",
                                    """{ \"date_from\": \"""" + today +
                                    """\", \"date_to\": \"""" + today + """\", \"dimension\": [ \"modelID\" ], \"filters\": [ { \"key\": \"string\", \"op\": \"EQ\", \"value\": \"string\" } ], \"limit\": 100, \"metrics\": [ \"ordered_units\", \"revenue\", \"delivered_units\", \"postings\", \"returns\", \"cancellations\", \"hits_view_pdp\", \"hits_tocart\" ], \"offset\": 0}"""),
        # seven days analytics data
        'v1_analytics_data_from_six_days_ago_to_today': ("/v1/analytics/data",
                                                         """{ \"date_from\": \"""" + six_days_ago +
                                                         """\", \"date_to\": \"""" + today + """\", \"dimension\": [ \"modelID\" ], \"filters\": [ { \"key\": \"string\", \"op\": \"EQ\", \"value\": \"string\" } ], \"limit\": 100, \"metrics\": [ \"ordered_units\", \"revenue\", \"delivered_units\", \"postings\", \"returns\", \"cancellations\", \"hits_view_pdp\", \"hits_tocart\" ], \"offset\": 0}"""),
        # for yesterday data
        'v1_analytics_data_day_ago': ("/v1/analytics/data",
                                      """{ \"date_from\": \"""" + day_ago +
                                      """\", \"date_to\": \"""" + day_ago + """\", \"dimension\": [ \"modelID\" ], \"filters\": [ { \"key\": \"string\", \"op\": \"EQ\", \"value\": \"string\" } ], \"limit\": 100, \"metrics\": [ \"ordered_units\", \"revenue\", \"delivered_units\", \"postings\", \"returns\", \"cancellations\", \"hits_view_pdp\", \"hits_tocart\" ], \"offset\": 0}"""),
        # past week
        'v1_analytics_data_from_thirteen_days_ago_to_seven_days_ago': ("/v1/analytics/data",
                                                                       """{ \"date_from\": \"""" + thirteen_days_ago +
                                                                       """\", \"date_to\": \"""" + seven_days_ago + """\", \"dimension\": [ \"modelID\" ], \"filters\": [ { \"key\": \"string\", \"op\": \"EQ\", \"value\": \"string\" } ], \"limit\": 100, \"metrics\": [ \"ordered_units\", \"revenue\", \"delivered_units\", \"postings\", \"returns\", \"cancellations\", \"hits_view_pdp\", \"hits_tocart\" ], \"offset\": 0}"""),

    }
    day_methods = {
        # past month
        'v2_finance_transaction_month_from_month_ago_to_today': ("/v2/finance/transaction/list",
                                                                 """{ \"filter\": { \"date\": { \"from\": \"""" +
                                                                 month_ago + """T00:00:00.001Z\", \"to\": \"""" +
                                                                 today + """T23:59:59.626Z\" }, \"posting_number\": \"\", \"transaction_type\": \"all\" }, \"page\": 1, \"page_size\": 100000}"""),
        'v1_stock_on_warehouses': ("/v1/analytics/stock_on_warehouses",
                                   "{ \"limit\": 1000, \"offset\": 0}"),
        'v2_posting_fbo_delivered_from_thirteen_days_ago_to_today': ("/v2/posting/fbo/list",
                                                                     """{ \"dir\": \"desc\", \"filter\": { \"since\": \"""" + thirteen_days_ago +
                                                                     """T00:00:00.000Z\", \"status\": \"delivered\", \"to\": \"""" + today +
                                                                     """T16:30:15.734Z\" }, \"limit\": 1000, \"offset\": 0, \"translit\": true, \"with\": { \"analytics_data\": true, \"financial_data\": true }}"""),
        'v2_posting_fbo_delivering_from_thirteen_days_ago_to_today': ("/v2/posting/fbo/list",
                                                                      """{ \"dir\": \"desc\", \"filter\": { \"since\": \"""" + thirteen_days_ago +
                                                                      """T00:00:00.000Z\", \"status\": \"delivering\", \"to\": \"""" + today +
                                                                      """T16:30:15.734Z\" }, \"limit\": 1000, \"offset\": 0, \"translit\": true, \"with\": { \"analytics_data\": true, \"financial_data\": true }}"""),
        'v2_posting_fbo_delivered_from_month_ago_to_today': ("/v2/posting/fbo/list",
                                                             """{ \"dir\": \"desc\", \"filter\": { \"since\": \"""" + month_ago +
                                                             """T00:00:00.000Z\", \"status\": \"delivered\", \"to\": \"""" + today +
                                                             """T16:30:15.734Z\" }, \"limit\": 1000, \"offset\": 0, \"translit\": true, \"with\": { \"analytics_data\": true, \"financial_data\": true }}"""),
    }

    methods = {
        "hours": hours_methods,
        "day": day_methods
    }
    return methods

import calculations.services.calculations.analytics.processing.extracting as extract
import calculations.services.calculations.analytics.processing.data_processing as dap
import calculations.services.calculations.algorithms.advanced_data_processing as adap


def extract_class():
    extract_class_dict = {'v1_analytics_data': extract.V1AnalyticsData,
                          'v2_finance_transaction': extract.V2FinanceTransaction,
                          'v1_stock_on_warehouses': extract.V1StockOnWarehouses,
                          'v2_posting_fbo': extract.V2PostingFbo}
    return extract_class_dict


def metric_class():
    metric_class_dict = {'common_user_info': dap.CommonUserInfo,
                         'supplies_info': dap.SuppliesInfo,
                         'abc': dap.Abc}
    return metric_class_dict


def get_report_place():
    report_place = {'v1_analytics_data_today': 'hours',
                    'v1_analytics_data_from_six_days_ago_to_today': 'hours',
                    'v1_analytics_data_day_ago': 'hours',
                    'v1_analytics_data_from_thirteen_days_ago_to_seven_days_ago': 'hours',
                    'v2_finance_transaction_month_from_month_ago_to_today': 'day',
                    'v1_stock_on_warehouses': 'day',
                    'v2_posting_fbo_delivered_from_thirteen_days_ago_to_today': 'day',
                    'v2_posting_fbo_delivering_from_thirteen_days_ago_to_today': 'day',
                    'v2_posting_fbo_delivered_from_month_ago_to_today': 'day'}
    return report_place

from calculations.services.calculations.analytics.supporting_func.distribution import definite_files_for_read, \
    pass_request_to_extracting, pass_request_to_processing
from calculations.services.calculations.analytics.supporting_func.initialization import *
from calculations.services.calculations.supporting.error_processing import *


@process_error_in_main_func
def common_user_info(client_id):
    request = {METRIC: 'common_user_info', TYPES_OF_REPORT: {
        V1_ANALYTICS_DATA: {V1_ANALYTICS_DATA_TODAY: 0, V1_ANALYTICS_DATA_FROM_SIX_DAYS_AGO_TO_TODAY: 0,
                            V1_ANALYTICS_DATA_DAY_AGO: 0,
                            V1_ANALYTICS_DATA_FROM_THIRTEEN_DAYS_AGO_TO_SEVEN_DAYS_AGO: 0},
        V2_FINANCE_TRANSACTION: {V2_FINANCE_TRANSACTION_MONTH_FROM_MONTH_AGO_TO_TODAY: 0}},
               INPUT_DATA: {}}
    request_report_data = definite_files_for_read(client_id, request)
    request_with_data = pass_request_to_extracting(request, request_report_data)
    common_user_info = pass_request_to_processing(request_with_data)
    return common_user_info


@process_error_in_main_func
def supplies_info(client_id):
    request = {METRIC: 'supplies_info', TYPES_OF_REPORT: {
        V1_STOCK_ON_WAREHOUSES: {V1_STOCK_ON_WAREHOUSES: 0},
        V2_POSTING_FBO: {V2_POSTING_FBO_DELIVERED_FROM_THIRTEEN_DAYS_AGO_TO_TODAY: 0,
                         V2_POSTING_FBO_DELIVERING_FROM_THIRTEEN_DAYS_AGO_TO_TODAY: 0}},
               INPUT_DATA: {}}
    request_report_data = definite_files_for_read(client_id, request)
    request_with_data = pass_request_to_extracting(request, request_report_data)
    supplies_info = pass_request_to_processing(request_with_data)
    return supplies_info


@process_error_in_main_func
def abc(client_id):
    request = {METRIC: 'abc', TYPES_OF_REPORT: {
        V1_STOCK_ON_WAREHOUSES: {V1_STOCK_ON_WAREHOUSES: 0},
        V2_POSTING_FBO: {V2_POSTING_FBO_DELIVERED_FROM_MONTH_AGO_TO_TODAY: 0}},
               INPUT_DATA: {}}
    request_report_data = definite_files_for_read(client_id, request)
    request_with_data = pass_request_to_extracting(request, request_report_data)
    abc = pass_request_to_processing(request_with_data)
    return abc

from analytics.settings import BASE_DIR
from os.path import join
import json
from calculations.services.calculations.analytics.supporting_func.initialization import *
from calculations.services.calculations.analytics.supporting_func.definition import extract_class, metric_class, \
    get_report_place
from calculations.services.calculations.supporting.error_processing import *


def definite_files_for_read(client_id, request):
    place_data_dict = {}  # Словарь где хранится ключ filename и его значение
    request_report_place = {}  # Словарь где хранится ключ report и место где он лежит
    request_report_data = {}  # Словарь где хранится ключ report и его данные
    report_place = get_report_place()  # Сначала получим словарь, где прописано где лежит каждый отчет

    for type in request[TYPES_OF_REPORT]:
        for report in request[TYPES_OF_REPORT][type]:
            request_report_place[report] = report_place[
                report]  # Сформируем такой же словарь как выше, но для тех отчетов что в запросе

    for filename in request_report_place.values():  # Формируем словарь из тех мест где хранятся отчеты запроса
        place_data_dict[filename] = 0

    for filename in place_data_dict:  # Заполняем словарь из тех мест где хранятся отчеты запроса
        try:
            with open(join(BASE_DIR, f'data/{client_id}/{filename}.json'), 'r') as file:
                place_data_dict[filename] = json.load(file)
        except Exception as ex:
            loggers.logger.error(f"Getting file error: {ex} for filename {filename} for client_id {client_id}")
            raise GettingReportError('Getting file error!')
    for report in request_report_place:  # Делаем финальный словарь
        try:
            request_report_data[report] = place_data_dict[request_report_place[report]][report]
        except Exception as ex:
            loggers.logger.error(f"Getting report error: {ex} for report {report} for client_id {client_id} ")
            raise GettingReportError(f'Getting report error!')
    return request_report_data


def pass_request_to_extracting(request, report_data):
    extract_class_dict = extract_class()
    for type_of_report in request[TYPES_OF_REPORT].keys():
        for report in request[TYPES_OF_REPORT][type_of_report]:
            request[TYPES_OF_REPORT][type_of_report][report] = extract_class_dict[type_of_report](
                data=report_data[report])
            request[TYPES_OF_REPORT][type_of_report][report].run()
    return request


def pass_request_to_processing(request_with_data):
    metric_class_dict = metric_class()
    metric_data = {TYPES_OF_REPORT: request_with_data[TYPES_OF_REPORT], INPUT_DATA: request_with_data[INPUT_DATA]}
    metric = metric_class_dict[request_with_data[METRIC]](metric_data=metric_data)
    db = metric.run()
    return db

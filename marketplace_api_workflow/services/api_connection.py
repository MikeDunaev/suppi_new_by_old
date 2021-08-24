from marketplace_api_workflow.services.ozon_api_connection import _connect
from marketplace_api_workflow.services.pars import _Parser
from marketplace_api_workflow.services.group_requests import _adjust_requests
import logging
logger = logging.getLogger(__name__)

def data_from_api(api_key: str, client_id: str, interval='all'):
    """
    Основной метод работы с апи, связывает все подметоды.
    Варианты интервалов: hours, day, all
    """
    try:
        methods = _adjust_requests()
    except Exception as ex:
        logger.error(f'Ошибка при формировании групп отчетов для получения данных с ozon. Подробнее об ошибке: {ex}')

    try:
        if interval == 'hours' or interval == 'all':
            data = _connect(methods=methods['hours'], api_key=api_key, client_id=client_id)
            parser = _Parser(filename='hours', data=data, client_id=client_id)
            parser.run()
    except Exception as ex:
        logger.error(f'Ошибка загрузки данных группы {interval} с ozon. Подробнее об ошибке: {ex}')

    try:
        if interval == 'day' or interval == 'all':
            data = _connect(methods=methods['day'], api_key=api_key, client_id=client_id)
            parser = _Parser(filename='day', data=data, client_id=client_id)
            parser.run()
    except Exception as ex:
        logger.error(f'Ошибка загрузки данных группы {interval} с ozon. Подробнее об ошибке: {ex}')


if __name__ == '__main__':
    data_from_api(api_key='f7455138-aae6-4d2e-8e79-b03919f99cb7', client_id='12849', interval='all')
    data_from_api(api_key='d94523cd-b1ca-4c2e-bb26-795aa8f25c1f', client_id='80079', interval='all')

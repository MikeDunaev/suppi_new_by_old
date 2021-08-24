import requests
from requests.exceptions import HTTPError
import logging
logger = logging.getLogger(__name__)

def _connect(methods: list, api_key: str, client_id: str) -> list:
    """ Скачивает данные с API Ozon.
    На вход принимает список методов, по которым нужно сделать запросы.

    """
    api_key = api_key
    client_id = client_id
    _data = {}
    _headers = {
        "content-type": "application/json",
        "Host": "api-seller.ozon.ru",
        "Client-Id": client_id,
        "Api-Key": api_key
    }
    _success_count = 0

    for i in methods.keys():
        try:
            url = "https://api-seller.ozon.ru" + methods[i][0]
            response = requests.post(url,
                                     headers=_headers,
                                     data=methods[i][1])

            # если ответ успешен, исключения задействованы не будут
            response.raise_for_status()

            _data[i] = response.json()
            _success_count += 1

        except HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            logger.error(f'Other error occurred: {err}')
    if _success_count < len(methods):
        logger.error("Failed!")
    else:
        logger.info('Success!')

    return _data

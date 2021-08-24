import json
from os.path import join, isdir
from os import mkdir
from analytics.settings import BASE_DIR
import logging
logger = logging.getLogger(__name__)

class _Parser:
    """ Первый парсер для придания json файлам вид нормальной вложенной структуры.
    path: путь к файлу, который нужно пропарсить.
    """

    def __init__(self, filename: str, data: list, client_id: str):
        self.path = join(BASE_DIR, f'api_workflow/services/{filename}.json')
        self.filename = filename
        self.raw_json = data
        self.client_id = client_id
        self.results = []
        self.processed_data = []


    def _save(self):
        """
        Если парсинг успешен - сохраняет данные в папку data.
        Название файла зависит от данных (дневной json или месячный).
        """
        if not isdir(join(BASE_DIR, f'data/{self.client_id}')):
            try:
                mkdir(join(BASE_DIR, f'data/{self.client_id}'))
            except Exception as ex:
                logger.error(f'Ошибка создания директория: {ex}')
        try:
            with open(join(BASE_DIR, f'data/{self.client_id}/{self.filename}.json'),
                      'w') as file:
                json.dump(self.raw_json, file, indent=3)
        except Exception as ex:
            logger.error(f'Ошибка сохранения после парсинга: {ex}')

    def run(self):
        self._save()

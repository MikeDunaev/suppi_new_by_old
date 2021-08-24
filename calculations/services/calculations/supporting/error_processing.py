from calculations.services.calculations.supporting import loggers


class GettingReportError(Exception):
    def __init__(self, text):
        self.txt = text


class EmptyData(Exception):
    def __init__(self, text):
        self.txt = text


def process_error_in_main_func(main_func):
    def wrapper(client_id):  # Функция обертка
        try:
            db = main_func(client_id)
        except GettingReportError:
            raise Exception
        except EmptyData:
            raise Exception
        except Exception as ex:
            loggers.logger.error(f'Exception occurred for client {client_id}', exc_info=True)
            raise Exception
        else:
            return db

    return wrapper

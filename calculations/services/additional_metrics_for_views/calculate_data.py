from calculations.db_connector import calculate_data_from_api
from marketplace_api_workflow.services.api_connection import data_from_api


def create_or_update_data_for_shop(current_shop, api_key, interval):
    """
    Проверяет наличие зарегистрированного магазина у продавца. В случае успешной проверки обновляет данные,
    в противном случае проверяет наличие демо данных в бд.
    """
    if int(current_shop) != 0:
        data_from_api(api_key=api_key, client_id=str(current_shop), interval=interval)
        pass

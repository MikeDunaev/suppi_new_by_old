from calculations.services.additional_metrics_for_views.connector_methods import \
    db_create_new_supplies_data, db_create_new_main_analytic_data, db_create_new_abc_data
from .services.additional_metrics_for_views.getting_data import get_calculated_data


def calculate_data_from_api(current_shop):
    """Сохраняет расчетные данные в бд"""

    main_page, supplies_info, abc = get_calculated_data(str(current_shop))

    saving_data_to_db_if_not_0(current_shop, main_page, supplies_info, abc)



def saving_data_to_db_if_not_0(client_id, main_page, supplies_info, abc):
    """Проверяет присутствие данных по продавцу в бд, исходя из этого обновляет или создает данные в бд"""

    if main_page != '0':
        db_create_new_main_analytic_data(client_id, main_page=main_page)

    if supplies_info != '0':
        db_create_new_supplies_data(client_id, supplies_info=supplies_info)

    if abc != '0':
        db_create_new_abc_data(client_id, abc=abc)

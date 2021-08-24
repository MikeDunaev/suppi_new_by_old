from calculations.models import Main_analytic, Supplies_info, ABC
import logging

logger = logging.getLogger(__name__)

def db_create_new_main_analytic_data(client_id, main_page):
    def create_main_analytic(client_id, main_page, item):
        main_analyt = Main_analytic(ordered_rub=main_page[item]['ordered_rub'],
                                    ordered_thing=main_page[item]['ordered_thing'],
                                    ordered_percent_rub=main_page[item]['ordered_percent_rub'],
                                    ordered_percent_thing=main_page[item]['ordered_percent_thing'],

                                    redeemed_rub=main_page[item]['redeemed_rub'],
                                    redeemed_percent_rub=main_page[item]['redeemed_percent_rub'],

                                    proceeds_rub=main_page[item]['proceeds_rub'],
                                    proceeds_percent_rub=main_page[item]['proceeds_percent_rub'],

                                    cancelled_thing=main_page[item]['cancelled_thing'],
                                    cancelled_percent_thing=main_page[item]['cancelled_percent_thing'],

                                    refund_thing=main_page[item]['refund_thing'],
                                    refund_percent_thing=main_page[item]['refund_percent_thing'],

                                    views_thing=main_page[item]['views_thing'],
                                    views_percent=main_page[item]['views_percent'],

                                    to_cart_thing=main_page[item]['to_cart_thing'],
                                    to_cart_percent=main_page[item]['to_cart_percent'],

                                    shop=client_id)
        return main_analyt

    try:
        Main_analytic.objects.filter(shop=client_id).delete()
        main_analytic_data = []
        for analytic_data in range(len(main_page)):
            main_analytic_data.append(create_main_analytic(client_id, main_page, item=analytic_data))
        Main_analytic.objects.bulk_create(main_analytic_data)

    except Exception as ex:
        logger.error(f'Ошибка загрузки данных в таблицу calculations_main_analytic. Подробнее об ошибке: {ex}')


def db_create_new_supplies_data(client_id, supplies_info):
    def create_supplies(client_id, item):
        supplies = Supplies_info(warehouse=item['warehouse'],
                                 sku=item['sku'],
                                 product=item['product'],
                                 days_left=item['days_left'],
                                 remains=item['remains'],
                                 total_warehouse_remains=item['total_warehouse_remains'],
                                 selling_speed=item['selling_speed'],
                                 total_product_selling_speed=item['total_product_selling_speed'],

                                 shop=client_id)
        return supplies

    try:
        Supplies_info.objects.filter(shop=client_id).delete()
        supplies_info_data = []
        for suppl in supplies_info:
            supplies_info_data.append(create_supplies(client_id, item=suppl))
        Supplies_info.objects.bulk_create(supplies_info_data)
    except Exception as ex:
        logger.error(f'Ошибка загрузки данных в таблицу calculations_supplies_info. Подробнее об ошибке: {ex}')


def db_create_new_abc_data(client_id, abc):
    def create_abc(client_id, item):
        abc_data = ABC(product=item['product'],
                       warehouse=item['warehouse'],
                       offer_id=item['offer_id'],

                       purchased_product=item['purchased_product'],
                       purchased_product_warehouse=item['purchased_product_warehouse'],
                       purchased_warehouse=item['purchased_warehouse'],

                       proceeds_product=item['proceeds_product'],
                       proceeds_product_warehouse=item['proceeds_product_warehouse'],
                       proceeds_warehouse=item['proceeds_warehouse'],

                       proceeds_product_percent=item['proceeds_product_percent'],
                       proceeds_product_warehouse_percent=item['proceeds_product_warehouse_percent'],
                       proceeds_warehouse_percent=item['proceeds_warehouse_percent'],

                       abc_products=item['abc_products'],
                       abc_product_warehouse=item['abc_product_warehouse'],
                       abc_warehouse=item['abc_warehouse'],

                       shop=client_id)
        return abc_data

    try:
        ABC.objects.filter(shop=client_id).delete()
        abc_data_list = []
        for abc_item in abc:
            abc_data_list.append(create_abc(client_id, item=abc_item))
        ABC.objects.bulk_create(abc_data_list)

    except Exception as ex:
        logger.error(f'Ошибка загрузки данных в таблицу calculations_abc. Подробнее об ошибке: {ex}')

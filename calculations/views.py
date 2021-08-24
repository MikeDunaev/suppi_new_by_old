from django.shortcuts import render
from .models import *
from .services.additional_metrics_for_views.supplies_info import addition_metrics_for_supplies_info
from .services.additional_metrics_for_views.get_seller import get_seller_and_current_shop
from .tasks import update_data_from_api_day, update_data_from_api_hours
from .db_connector import calculate_data_from_api
import logging

logger = logging.getLogger(__name__)


def index(request):
    # """Отвечает за отображение главной страницы сайта"""
    user = request.user

    if not user.is_authenticated:
        return render(request, template_name='calculations/landingpage.html')

    seller, shop = get_seller_and_current_shop(username=user)

    update_seller_data(seller.current_shop, shop.api_key)

    try:
        unique_warehouses, amount_of_non_unique_warehouses = addition_metrics_for_supplies_info()
    except Exception as ex:
        logger.error(f'Ошибка при рассчетах дополнительных метрик для контекста отображения. Подробнее об ошибке: {ex}')

    if seller.current_shop != 0:
        main_page = Main_analytic.objects.filter(shop=seller.current_shop)
    else:
        main_page = 0, 0
    context = {
        'final_main_page_day': main_page[:1],
        'final_main_page_week': main_page[1:2],
        'supplies_info': Supplies_info.objects.filter(shop=seller.current_shop),
        'warehouses': unique_warehouses,
        'amount_of_non_unique_warehouses': amount_of_non_unique_warehouses,
        'abc': ABC.objects.filter(shop=seller.current_shop),
        'shop': seller.current_shop,
        'user': user
    }

    return render(request, template_name='calculations/index3.html', context=context)


def update_seller_data(current_shop, api_key):
    update_data_from_api_day(current_shop=current_shop, api_key=api_key)
    update_data_from_api_hours(current_shop=current_shop, api_key=api_key)
    try:
            calculate_data_from_api(current_shop=current_shop)
    except Exception as ex:
        logger.error(f"Обновление данных отменено. Ошибка: {ex}")

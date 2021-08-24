
from calculations.services.additional_metrics_for_views.calculate_data import create_or_update_data_for_shop


#@app.task(default_retry_delay=60)
def update_data_from_api_hours(current_shop, api_key):
    create_or_update_data_for_shop(current_shop=current_shop, api_key=api_key, interval='hours')


#@app.task(default_retry_delay=600)
def update_data_from_api_day(current_shop, api_key):
    create_or_update_data_for_shop(current_shop=current_shop, api_key=api_key, interval='day')
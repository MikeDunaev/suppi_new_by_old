from calculations.services.calculations.output_db import common_user_info as final_main_page
from calculations.services.calculations.output_db import abc as ABC_data
from calculations.services.calculations.output_db import supplies_info
import logging
logger = logging.getLogger(__name__)

def get_calculated_data(client_id: str) -> tuple:
    if int(client_id) == 0:
        logger.info("client_id = 0")
        main_page, supplies, abc = '0', '0', '0'
    else:
        main_page = final_main_page(client_id)
        supplies = supplies_info(client_id)
        abc = ABC_data(client_id)

    return main_page, supplies, abc


import math


def get_proceed_from_price_minus_commission_percent(price, commision_percent):
    proceed = price * (100 - commision_percent) / 100
    return proceed

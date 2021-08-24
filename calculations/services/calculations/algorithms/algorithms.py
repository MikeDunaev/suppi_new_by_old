import numpy as np
import pandas as pd
from calculations.services.calculations.supporting.error_processing import *
import calculations.services.calculations.supporting.math_func as mat


def calculate_days_to_left(remains, selling_speed):
    if remains == 0:
        return 'Закончился'
    elif selling_speed == 0:
        return 'Нет продаж'
    else:
        return remains / selling_speed


def calculate_days_to_left_interval(remains):
    if type(remains) == int or type(remains) == float:
        if 2 >= remains > 0:
            return '1-2'
        elif 2 < remains < 5:
            return f" {round(remains - 1)}-{round(remains + 1)}"
        elif 5 <= remains < 10:
            return f"{round(remains - 2)}-{round(remains + 2)}"
        elif 10 <= remains < 30:
            return f"{round(remains - remains * 0.2)}-{round(remains + remains * 0.2)}"
        else:
            return f"{round(remains - remains * (0.2 - 0.00068 * (remains - 30)))}-{round(remains + remains * (0.2 - 0.00068 * (remains - 30)))}"
    else:
        return remains


def assign_abc_category(accumulated_percent, percent):
    a_category_percent = 81
    b_category_percent = 95
    c_category_percent = 100 - b_category_percent
    if percent == np.nan:
        category = 'C'
    else:
        if accumulated_percent < a_category_percent and accumulated_percent != 0:
            category = 'A'
        else:
            if accumulated_percent < b_category_percent and accumulated_percent != 0:
                category = 'B'
            else:
                if percent > c_category_percent:
                    category = 'B'
                else:
                    category = 'C'
    return category

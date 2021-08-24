import datetime
import numpy as np
import pandas as pd
from calculations.services.calculations.analytics.supporting_func.initialization import *
from calculations.services.calculations.supporting.error_processing import *
import calculations.services.calculations.supporting.math_func as mat
import calculations.services.calculations.algorithms.algorithms as algo


class V1AnalyticsData:
    pass


class V2FinanceTransaction:
    def __init__(self, table, from_day, to_day):
        self.finance_transaction_table = table
        self.from_day = datetime.date.today() - datetime.timedelta(days=(1 + from_day))
        self.to_day = datetime.date.today() - datetime.timedelta(days=(1 + to_day))
        self.transaction_table_from_day_to_day = None
        self.transaction_table_with_delivered_status = None
        self.order_amount_sum = None
        self.total_amount_sum = None

    def get_transaction_table_from_day_to_day(self):
        self.transaction_table_from_day_to_day = self.finance_transaction_table[
            (self.finance_transaction_table[TRANDATE] >= pd.Timestamp(self.from_day))]
        self.transaction_table_from_day_to_day = self.transaction_table_from_day_to_day[(
                self.transaction_table_from_day_to_day[TRANDATE] <= pd.Timestamp(self.to_day))]
        self.transaction_table_from_day_to_day.reset_index(drop=True, inplace=True)

    def get_transaction_table_with_delivered_status(self):
        self.get_transaction_table_from_day_to_day()
        self.transaction_table_with_delivered_status = self.transaction_table_from_day_to_day.groupby(
            ORDERSTATE).get_group(DELIVERED_RUS)
        self.transaction_table_with_delivered_status.reset_index(drop=True, inplace=True)

    def get_order_and_total_amount_delivered_sum(self):
        self.get_transaction_table_with_delivered_status()
        self.order_amount_sum = self.transaction_table_with_delivered_status[ORDERAMOUNT].sum()
        self.total_amount_sum = self.transaction_table_with_delivered_status[TOTALAMOUNT].sum()


class V1StockOnWarehouses:
    def __init__(self, warehouse_remains_table=None, total_product_remains_table=None):
        self.warehouse_remains_table = warehouse_remains_table
        self.total_product_remains_table = total_product_remains_table  # None, потому что что-то может понадобиться а что то нет
        self.get_warehouse_remains_table_with_common_offer_id_func_flag = False
        self.warehouse_remains_table_with_common_offer_id = None
        self.offer_id_official = None
        self.warehouse_name_official = None
        self.warehouse_total_remains_on_warehouse = None
        self.warehouse_total_remains_on_product_with_common_offer_id = None

    def get_warehouse_remains_table_with_standard(self):
        self.warehouse_remains_table_with_standard = self.warehouse_remains_table.copy()
        self.warehouse_remains_table_with_standard.loc[:, NAME] = self.warehouse_remains_table_with_standard[
            NAME].str.upper()
        self.warehouse_remains_table_with_standard.rename(columns={NAME: WAREHOUSE_NAME}, inplace=True)
        self.warehouse_remains_table_with_standard.loc[:, FOR_SALE].map(
            lambda row: 0 if row < 0 else row)  # Убрать отрицательные значения

    def get_warehouse_remains_table_with_common_offer_id(self):
        self.get_warehouse_remains_table_with_standard()
        self.warehouse_remains_table_with_common_offer_id = \
            self.warehouse_remains_table_with_standard.groupby([WAREHOUSE_NAME, OFFER_ID, TITLE], as_index=False)[
                FOR_SALE].sum()
        self.get_warehouse_remains_table_with_common_offer_id_func_flag = True

    def get_offer_id_and_warehouse_name_official(self):
        if not self.get_warehouse_remains_table_with_common_offer_id_func_flag:
            self.get_warehouse_remains_table_with_common_offer_id()
        self.offer_id_official = self.warehouse_remains_table_with_common_offer_id[OFFER_ID].unique()
        self.warehouse_name_official = self.warehouse_remains_table_with_common_offer_id[
            WAREHOUSE_NAME].unique()

    def get_warehouse_total_remains_on_warehouse(self):
        if not self.get_warehouse_remains_table_with_common_offer_id_func_flag:
            self.get_warehouse_remains_table_with_common_offer_id()
        self.warehouse_total_remains_on_warehouse = \
            self.warehouse_remains_table_with_common_offer_id.groupby(WAREHOUSE_NAME, as_index=False)[FOR_SALE].sum()

    def get_warehouse_total_remains_on_product_with_common_offer_id(self):
        self.warehouse_total_remains_on_product_with_common_offer_id = \
            self.total_product_remains_table.groupby([OFFER_ID, TITLE], as_index=False)[
                FOR_SALE].sum()


class V2PostingFbo:
    def __init__(self, table):
        self.fbo_table = table
        self.remove_unnecessary_warehouses_and_offer_id_func_flag = False
        self.fbo_table_with_common_offer_id = None
        self.fbo_table_without_unnecessary = None
        self.fbo_table_with_selling_speed = None
        self.fbo_table_with_proceeds_percent = None
        self.fbo_table_with_accumulated_percent = None
        self.warehouse_total_with_accumulated_percent = None
        self.product_total_with_accumulated_percent = None
        self.total_proceeds = None

    def get_fbo_table_with_standard(self):
        self.fbo_table_with_standard = self.fbo_table.copy()
        self.fbo_table_with_standard.loc[:, WAREHOUSE_NAME] = self.fbo_table_with_standard[
            WAREHOUSE_NAME].str.split('_').str.get(0)
        self.fbo_table_with_standard.rename(columns={NAME: TITLE}, inplace=True)
        self.fbo_table_with_standard[PROCEEDS] = self.fbo_table_with_standard[[PRICE, COMMISSION_PERCENT]].apply(
            lambda row: mat.get_proceed_from_price_minus_commission_percent(price=float(row[PRICE]),
                                                                            commision_percent=float(row[
                                                                                                        COMMISSION_PERCENT])),
            axis=1)

    def get_fbo_table_with_common_offer_id(self):
        self.get_fbo_table_with_standard()
        self.fbo_table_with_common_offer_id = self.fbo_table_with_standard.copy()
        self.fbo_table_with_common_offer_id = self.fbo_table_with_common_offer_id[
            self.fbo_table_with_common_offer_id[
                OFFER_ID] != '']  # Удалить столбы где продают услугу убрал отсюда .copy()
        self.fbo_table_with_common_offer_id = \
            self.fbo_table_with_common_offer_id.groupby([WAREHOUSE_NAME, OFFER_ID, TITLE], as_index=False)[
                [PROCEEDS, QUANTITY]].sum()

    def remove_unnecessary_warehouses_and_offer_id(self, offer_id_official, warehouse_name_official):
        self.offer_id_official = offer_id_official
        self.warehouse_name_official = warehouse_name_official
        self.get_fbo_table_with_common_offer_id()
        self.fbo_table_without_unnecessary = self.fbo_table_with_common_offer_id.copy()
        self.fbo_table_without_unnecessary = self.fbo_table_without_unnecessary.loc[
            self.fbo_table_without_unnecessary[OFFER_ID].isin(self.offer_id_official)].reset_index(
            drop=True)
        self.fbo_table_without_unnecessary = self.fbo_table_without_unnecessary.loc[
            self.fbo_table_without_unnecessary[WAREHOUSE_NAME].isin(self.warehouse_name_official)].reset_index(
            drop=True)
        self.remove_unnecessary_warehouses_and_offer_id_func_flag = True

    def get_fbo_table_with_selling_speed(self, offer_id_official, warehouse_name_official, days):
        if not self.remove_unnecessary_warehouses_and_offer_id_func_flag:
            self.remove_unnecessary_warehouses_and_offer_id(offer_id_official, warehouse_name_official)
        self.days = days
        self.fbo_table_with_selling_speed = self.fbo_table_without_unnecessary.copy()
        self.fbo_table_with_selling_speed[SELLING_SPEED] = self.fbo_table_with_selling_speed[QUANTITY] / self.days

    def get_fbo_table_with_proceeds_percent(self, offer_id_official, warehouse_name_official):
        if not self.remove_unnecessary_warehouses_and_offer_id_func_flag:
            self.remove_unnecessary_warehouses_and_offer_id(offer_id_official, warehouse_name_official)
        self.fbo_table_with_proceeds_percent = self.fbo_table_without_unnecessary.copy()
        proceeds_warehouse = self.fbo_table_with_proceeds_percent.groupby([WAREHOUSE_NAME], as_index=False)[
            PROCEEDS].sum()
        proceeds_warehouse_column = self.fbo_table_with_proceeds_percent[WAREHOUSE_NAME].map(
            proceeds_warehouse.set_index(WAREHOUSE_NAME)[PROCEEDS])
        self.fbo_table_with_proceeds_percent[PROCEEDS_PERCENT] = (self.fbo_table_with_proceeds_percent[
                                                                      PROCEEDS] / proceeds_warehouse_column) * 100

    def get_fbo_table_with_accumulated_percent(self, offer_id_official,
                                               warehouse_name_official):  # Вот тут можно потом разделить еще на составляющие функции
        self.get_fbo_table_with_proceeds_percent(offer_id_official, warehouse_name_official)
        self.fbo_table_with_accumulated_percent = self.fbo_table_with_proceeds_percent.copy()
        self.fbo_table_with_accumulated_percent = self.fbo_table_with_accumulated_percent.groupby(
            [WAREHOUSE_NAME]).apply(
            lambda row: row.sort_values([PROCEEDS_PERCENT], ascending=False)).reset_index(
            drop=True)  # Благодаря reset индекс мы получаем целый датафрейма, без него это были бы просто группы с ключами
        self.fbo_table_with_accumulated_percent[ACCUMULATED_PERCENT] = self.fbo_table_with_accumulated_percent.groupby(
            [WAREHOUSE_NAME]).apply(lambda row: row[PROCEEDS_PERCENT].expanding(min_periods=1).sum()).reset_index(
            drop=True)

        self.warehouse_total_with_accumulated_percent = \
            self.fbo_table_with_accumulated_percent.groupby([WAREHOUSE_NAME], as_index=False)[
                [PROCEEDS, QUANTITY]].sum()
        self.total_proceeds = self.warehouse_total_with_accumulated_percent[PROCEEDS].sum()
        self.warehouse_total_with_accumulated_percent[PROCEEDS_PERCENT] = (
                                                                                  self.warehouse_total_with_accumulated_percent[
                                                                                      PROCEEDS] / self.total_proceeds) * 100
        self.warehouse_total_with_accumulated_percent.sort_values(PROCEEDS_PERCENT, ascending=False, inplace=True)
        self.warehouse_total_with_accumulated_percent[ACCUMULATED_PERCENT] = \
            self.warehouse_total_with_accumulated_percent[PROCEEDS_PERCENT].expanding(
                min_periods=1).sum()
        self.warehouse_total_with_accumulated_percent.reset_index(drop=True, inplace=True)

        self.product_total_with_accumulated_percent = \
            self.fbo_table_with_accumulated_percent.groupby([OFFER_ID, TITLE], as_index=False)[
                [PROCEEDS, QUANTITY]].sum()
        self.product_total_with_accumulated_percent[PROCEEDS_PERCENT] = (
                (self.product_total_with_accumulated_percent[PROCEEDS] / self.total_proceeds) * 100)
        self.product_total_with_accumulated_percent.sort_values(PROCEEDS_PERCENT, ascending=False, inplace=True)
        self.product_total_with_accumulated_percent[ACCUMULATED_PERCENT] = self.product_total_with_accumulated_percent[
            PROCEEDS_PERCENT].expanding(
            min_periods=1).sum()
        self.product_total_with_accumulated_percent.reset_index(drop=True, inplace=True)

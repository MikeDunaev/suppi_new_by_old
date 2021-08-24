import numpy as np
import pandas as pd
import calculations.services.calculations.analytics.processing.report_processing as rep
from calculations.services.calculations.analytics.supporting_func.initialization import *
from calculations.services.calculations.supporting.error_processing import *
import calculations.services.calculations.supporting.math_func as mat
import calculations.services.calculations.algorithms.algorithms as algo


class CommonUserInfo:
    def __init__(self, metric_data: dict):
        self.reports = metric_data[TYPES_OF_REPORT]
        self.input_data = None  # Тут только те данные что передает мне пользователь (если передает), не мои данные ни в коем случае!
        self.report_types = {V1_ANALYTICS_DATA: rep.V1AnalyticsData,
                             V2_FINANCE_TRANSACTION: rep.V2FinanceTransaction}

    def get_daily_info(self):
        self.total_analytic_data_today_table = self.reports[V1_ANALYTICS_DATA][
            V1_ANALYTICS_DATA_TODAY].total_table
        self.total_analytic_data_day_ago_table = self.reports[V1_ANALYTICS_DATA][
            V1_ANALYTICS_DATA_DAY_AGO].total_table

        self.daily_info_table = pd.DataFrame(
            [self.total_analytic_data_today_table, self.total_analytic_data_day_ago_table],
            index=[TODAY, DAY_AGO]).T
        self.daily_info_table.drop(['toc', 'real'], axis=0, inplace=True)  # Лишние неизвестные метрики
        self.daily_info_table[PERCENT + '_' + TODAY] = (self.daily_info_table[TODAY] / self.daily_info_table[
            DAY_AGO] - 1) * 100
        self.daily_info_table = self.daily_info_table.replace(np.Inf, np.nan)
        self.daily_info_table = self.daily_info_table.fillna(0)

    def get_monthly_info(self):
        self.total_analytic_data_from_six_days_ago_to_today_table = self.reports[V1_ANALYTICS_DATA][
            V1_ANALYTICS_DATA_FROM_SIX_DAYS_AGO_TO_TODAY].total_table
        self.total_analytic_data_from_thirteen_days_ago_to_seven_days_ago_table = \
            self.reports[V1_ANALYTICS_DATA][
                V1_ANALYTICS_DATA_FROM_THIRTEEN_DAYS_AGO_TO_SEVEN_DAYS_AGO].total_table

        self.weekly_info_table = pd.DataFrame([self.total_analytic_data_from_six_days_ago_to_today_table,
                                               self.total_analytic_data_from_thirteen_days_ago_to_seven_days_ago_table],
                                              index=[WEEK, WEEK_AGO]).T
        self.weekly_info_table.drop(['toc', 'real'], axis=0, inplace=True)  # Лишние неизвестные метрики
        self.weekly_info_table[PERCENT + '_' + WEEK] = (self.weekly_info_table[WEEK] / self.weekly_info_table[
            WEEK_AGO] - 1) * 100
        self.weekly_info_table = self.weekly_info_table.replace(np.Inf, np.nan)
        self.weekly_info_table = self.weekly_info_table.fillna(0)

    def get_redeemed_and_proceeds(self):
        self.finance_transaction_for_week = self.report_types[V2_FINANCE_TRANSACTION](
            table=self.reports[V2_FINANCE_TRANSACTION][
                V2_FINANCE_TRANSACTION_MONTH_FROM_MONTH_AGO_TO_TODAY].transaction_table, from_day=6, to_day=0)

        self.finance_transaction_for_week.get_order_and_total_amount_delivered_sum()
        self.redeemed_for_week = self.finance_transaction_for_week.order_amount_sum
        self.proceeds_for_week = self.finance_transaction_for_week.total_amount_sum

    def create_structure(self):
        self.get_daily_info()
        self.get_monthly_info()
        self.get_redeemed_and_proceeds()
        self.db_common_user_info = [
            {
                "ordered_rub": self.daily_info_table[TODAY]["ordered_rub"],
                "ordered_thing": self.daily_info_table[TODAY]["ordered_thing"],
                "ordered_percent_rub": round(self.daily_info_table[PERCENT + '_' + TODAY]["ordered_rub"], 1),
                "ordered_percent_thing": round(self.daily_info_table[PERCENT + '_' + TODAY]["ordered_thing"], 1),

                "redeemed_rub": 0,
                "redeemed_percent_rub": 0,

                "proceeds_rub": 0,
                "proceeds_percent_rub": 0,

                "cancelled_thing": self.daily_info_table[TODAY]["cancelled_thing"],
                "cancelled_percent_thing": round(self.daily_info_table[PERCENT + '_' + TODAY]["cancelled_thing"], 1),

                "refund_thing": self.daily_info_table[TODAY]["refund_thing"],
                "refund_percent_thing": round(self.daily_info_table[PERCENT + '_' + TODAY]["refund_thing"], 1),

                "views_thing": self.daily_info_table[TODAY]["views_thing"],
                "views_percent": round(self.daily_info_table[PERCENT + '_' + TODAY]["views_thing"], 1),

                "to_cart_thing": self.daily_info_table[TODAY]["to_cart_thing"],
                "to_cart_percent": round(self.daily_info_table[PERCENT + '_' + TODAY]["to_cart_thing"], 1),
            },
            {
                "ordered_rub": self.weekly_info_table[WEEK]["ordered_rub"],
                "ordered_thing": self.weekly_info_table[WEEK]["ordered_thing"],
                "ordered_percent_rub": round(self.weekly_info_table[PERCENT + '_' + WEEK]["ordered_rub"], 1),
                "ordered_percent_thing": round(self.weekly_info_table[PERCENT + '_' + WEEK]["ordered_thing"], 1),

                "redeemed_rub": self.redeemed_for_week,
                "redeemed_percent_rub": 0,

                "proceeds_rub": self.proceeds_for_week,
                "proceeds_percent_rub": 0,

                "cancelled_thing": self.weekly_info_table[WEEK]["cancelled_thing"],
                "cancelled_percent_thing": round(self.weekly_info_table[PERCENT + '_' + WEEK]["cancelled_thing"], 1),

                "refund_thing": self.weekly_info_table[WEEK]["refund_thing"],
                "refund_percent_thing": round(self.weekly_info_table[PERCENT + '_' + WEEK]["refund_thing"], 1),

                "views_thing": self.weekly_info_table[WEEK]["views_thing"],
                "views_percent": round(self.weekly_info_table[PERCENT + '_' + WEEK]["views_thing"], 1),

                "to_cart_thing": self.weekly_info_table[WEEK]["to_cart_thing"],
                "to_cart_percent": round(self.weekly_info_table[PERCENT + '_' + WEEK]["to_cart_thing"], 1)
            }
        ]

    def run(self):
        self.create_structure()
        return self.db_common_user_info


class SuppliesInfo:
    def __init__(self, metric_data: dict):
        self.reports = metric_data[TYPES_OF_REPORT]
        self.input_data = None
        self.report_types = {V1_STOCK_ON_WAREHOUSES: rep.V1StockOnWarehouses,
                             V2_POSTING_FBO: rep.V2PostingFbo}

    def get_processing_reports(self):
        self.stock_on_warehouses = self.report_types[V1_STOCK_ON_WAREHOUSES](
            warehouse_remains_table=self.reports[V1_STOCK_ON_WAREHOUSES][
                V1_STOCK_ON_WAREHOUSES].warehouse_remains_table)
        self.v2_posting_fbo_delivered_from_thirteen_days_ago_to_today = self.report_types[V2_POSTING_FBO](
            table=self.reports[V2_POSTING_FBO][
                V2_POSTING_FBO_DELIVERED_FROM_THIRTEEN_DAYS_AGO_TO_TODAY].fbo_posting_table)

    def get_required_tables(self):
        self.get_processing_reports()
        self.stock_on_warehouses.get_warehouse_total_remains_on_warehouse()
        self.stock_on_warehouses.get_offer_id_and_warehouse_name_official()
        self.warehouse_name_official = self.stock_on_warehouses.warehouse_name_official
        self.offer_id_official = self.stock_on_warehouses.offer_id_official
        self.warehouse_total_remains_on_warehouse = self.stock_on_warehouses.warehouse_total_remains_on_warehouse
        self.warehouse_remains_table_with_common_offer_id = self.stock_on_warehouses.warehouse_remains_table_with_common_offer_id
        self.v2_posting_fbo_delivered_from_thirteen_days_ago_to_today.get_fbo_table_with_selling_speed(
            offer_id_official=self.offer_id_official, warehouse_name_official=self.warehouse_name_official, days=14)
        self.fbo_table_with_selling_speed = self.v2_posting_fbo_delivered_from_thirteen_days_ago_to_today.fbo_table_with_selling_speed

    def get_days_to_left_table(self):
        self.get_required_tables()
        self.days_to_left_table = pd.merge(self.warehouse_remains_table_with_common_offer_id,
                                           self.fbo_table_with_selling_speed,
                                           left_on=[WAREHOUSE_NAME, OFFER_ID, TITLE],
                                           right_on=[WAREHOUSE_NAME, OFFER_ID, TITLE],
                                           how='left')
        self.days_to_left_table.drop([PROCEEDS], axis=1, inplace=True)
        self.days_to_left_table = self.days_to_left_table.fillna(0)
        self.days_to_left_table[DAYS_LEFT] = self.days_to_left_table.apply(
            lambda row: algo.calculate_days_to_left(row[FOR_SALE], row[SELLING_SPEED]), axis=1)

        self.days_to_left_table['total_warehouse_remains'] = self.days_to_left_table[WAREHOUSE_NAME].map(
            self.warehouse_total_remains_on_warehouse.set_index(WAREHOUSE_NAME)[
                FOR_SALE])
        self.days_to_left_table['total_product_selling_speed'] = self.days_to_left_table[OFFER_ID].map(
            self.days_to_left_table.groupby([OFFER_ID, TITLE], as_index=False)[SELLING_SPEED].sum().set_index(OFFER_ID)[
                SELLING_SPEED])
        self.days_to_left_table.rename(
            columns={WAREHOUSE_NAME: 'warehouse', OFFER_ID: 'sku', TITLE: 'product', FOR_SALE: 'remains'}, inplace=True)
        self.days_to_left_table.drop([QUANTITY], axis=1, inplace=True)

    def get_days_to_left_with_interval_table(self):
        self.get_days_to_left_table()
        self.days_to_left_table.loc[:, DAYS_LEFT] = self.days_to_left_table[DAYS_LEFT].apply(
            algo.calculate_days_to_left_interval)

    def create_structure(self):
        self.get_days_to_left_with_interval_table()
        self.db_supplies_info = []
        for row_index, row in self.days_to_left_table.iterrows():
            self.db_supplies_info.append({
                "warehouse": row['warehouse'],
                "sku": row['sku'],
                "product": row['product'],
                "days_left": row['days_left'],
                "remains": row['remains'],
                "total_warehouse_remains": row['total_warehouse_remains'],
                "selling_speed": round(row['selling_speed'], 1),
                "total_product_selling_speed": round(row['total_product_selling_speed'], 1)
            })

    def run(self):
        self.create_structure()
        return self.db_supplies_info


class Abc:
    def __init__(self, metric_data: dict):
        self.reports = metric_data[TYPES_OF_REPORT]
        self.input_data = None
        self.report_types = {V1_STOCK_ON_WAREHOUSES: rep.V1StockOnWarehouses,
                             V2_POSTING_FBO: rep.V2PostingFbo}
        self.get_required_tables_func_flag = False

    def get_processing_reports(self):
        self.stock_on_warehouses = self.report_types[V1_STOCK_ON_WAREHOUSES](
            warehouse_remains_table=self.reports[V1_STOCK_ON_WAREHOUSES][
                V1_STOCK_ON_WAREHOUSES].warehouse_remains_table,
            total_product_remains_table=self.reports[V1_STOCK_ON_WAREHOUSES][
                V1_STOCK_ON_WAREHOUSES].total_product_remains_table)
        self.v2_posting_fbo_delivered_from_month_ago_to_today = self.report_types[V2_POSTING_FBO](
            table=self.reports[V2_POSTING_FBO][
                V2_POSTING_FBO_DELIVERED_FROM_MONTH_AGO_TO_TODAY].fbo_posting_table)

    def get_required_tables(self):
        self.get_processing_reports()
        self.stock_on_warehouses.get_offer_id_and_warehouse_name_official()
        self.stock_on_warehouses.get_warehouse_total_remains_on_warehouse()
        self.stock_on_warehouses.get_warehouse_total_remains_on_product_with_common_offer_id()
        self.warehouse_total_remains_on_product_with_common_offer_id = self.stock_on_warehouses.warehouse_total_remains_on_product_with_common_offer_id
        self.warehouse_name_official = self.stock_on_warehouses.warehouse_name_official
        self.offer_id_official = self.stock_on_warehouses.offer_id_official
        self.warehouse_remains_table_with_common_offer_id = self.stock_on_warehouses.warehouse_remains_table_with_common_offer_id
        self.warehouse_total_remains_on_warehouse = self.stock_on_warehouses.warehouse_total_remains_on_warehouse
        self.v2_posting_fbo_delivered_from_month_ago_to_today.get_fbo_table_with_accumulated_percent(
            offer_id_official=self.offer_id_official, warehouse_name_official=self.warehouse_name_official)
        self.fbo_table_with_accumulated_percent = self.v2_posting_fbo_delivered_from_month_ago_to_today.fbo_table_with_accumulated_percent
        self.warehouse_total_with_accumulated_percent = self.v2_posting_fbo_delivered_from_month_ago_to_today.warehouse_total_with_accumulated_percent
        self.product_total_with_accumulated_percent = self.v2_posting_fbo_delivered_from_month_ago_to_today.product_total_with_accumulated_percent
        self.get_required_tables_func_flag = True

    def get_common_abc_analytic(self, missing_elements=True):
        if not self.get_required_tables_func_flag:
            self.get_required_tables()
        self.fbo_table_with_abc = self.fbo_table_with_accumulated_percent.copy()
        self.fbo_table_with_abc[CATEGORY] = self.fbo_table_with_abc.apply(
            lambda row: algo.assign_abc_category(row[ACCUMULATED_PERCENT], row[PROCEEDS_PERCENT]), axis=1)
        if missing_elements:
            self.fbo_table_with_abc_with_missing_elements = pd.merge(
                self.warehouse_remains_table_with_common_offer_id[[WAREHOUSE_NAME, OFFER_ID, TITLE]],
                self.fbo_table_with_abc,
                left_on=[WAREHOUSE_NAME, OFFER_ID, TITLE],
                right_on=[WAREHOUSE_NAME, OFFER_ID, TITLE], how='left')
            self.fbo_table_with_abc_with_missing_elements[CATEGORY].fillna('C', inplace=True)
            self.fbo_table_with_abc_with_missing_elements.fillna(0, inplace=True)

    def get_product_abc_analytic(self, missing_elements=True):
        if not self.get_required_tables_func_flag:
            self.get_required_tables()
        self.product_total_with_abc = self.product_total_with_accumulated_percent.copy()
        self.product_total_with_abc[CATEGORY] = self.product_total_with_abc.apply(
            lambda row: algo.assign_abc_category(row[ACCUMULATED_PERCENT], row[PROCEEDS_PERCENT]),
            axis=1)
        if missing_elements:
            self.product_total_with_abc_with_missing_elements = pd.merge(
                self.warehouse_total_remains_on_product_with_common_offer_id,
                self.product_total_with_abc,
                left_on=[OFFER_ID, TITLE],
                right_on=[OFFER_ID, TITLE],
                how='left')
            self.product_total_with_abc_with_missing_elements[CATEGORY].fillna('C', inplace=True)
            self.product_total_with_abc_with_missing_elements.fillna(0, inplace=True)

    def get_warehouse_abc_analytic(self, missing_elements=True):
        if not self.get_required_tables_func_flag:
            self.get_required_tables()
        self.warehouse_total_with_abc = self.warehouse_total_with_accumulated_percent.copy()
        self.warehouse_total_with_abc[CATEGORY] = self.warehouse_total_with_abc.apply(
            lambda row: algo.assign_abc_category(row[ACCUMULATED_PERCENT], row[PROCEEDS_PERCENT]), axis=1)
        if missing_elements:
            self.warehouse_total_with_abc_with_missing_elements = pd.merge(self.warehouse_total_remains_on_warehouse,
                                                                           self.warehouse_total_with_abc,
                                                                           left_on=[WAREHOUSE_NAME],
                                                                           right_on=[WAREHOUSE_NAME], how='left')
            self.warehouse_total_with_abc_with_missing_elements[CATEGORY].fillna('C', inplace=True)
            self.warehouse_total_with_abc_with_missing_elements.fillna(0, inplace=True)

    def create_main_table_for_structure(self):
        self.get_common_abc_analytic(missing_elements=True)
        self.get_product_abc_analytic(missing_elements=True)
        self.get_warehouse_abc_analytic(missing_elements=True)
        self.main_abc_table = self.fbo_table_with_abc_with_missing_elements.copy()

        self.main_abc_table['purchased_warehouse'] = self.main_abc_table[WAREHOUSE_NAME].map(
            self.warehouse_total_with_abc_with_missing_elements.set_index(WAREHOUSE_NAME)[QUANTITY])
        self.main_abc_table['purchased_product'] = self.main_abc_table[OFFER_ID].map(
            self.product_total_with_abc_with_missing_elements.set_index(OFFER_ID)[QUANTITY])
        self.main_abc_table['proceeds_warehouse'] = self.main_abc_table[WAREHOUSE_NAME].map(
            self.warehouse_total_with_abc_with_missing_elements.set_index(WAREHOUSE_NAME)[PROCEEDS])
        self.main_abc_table['proceeds_product'] = self.main_abc_table[OFFER_ID].map(
            self.product_total_with_abc_with_missing_elements.set_index(OFFER_ID)[PROCEEDS])
        self.main_abc_table['proceeds_warehouse_percent'] = self.main_abc_table[WAREHOUSE_NAME].map(
            self.warehouse_total_with_abc_with_missing_elements.set_index(WAREHOUSE_NAME)[PROCEEDS_PERCENT])
        self.main_abc_table['proceeds_product_percent'] = self.main_abc_table[OFFER_ID].map(
            self.product_total_with_abc_with_missing_elements.set_index(OFFER_ID)[PROCEEDS_PERCENT])
        self.main_abc_table['abc_warehouse'] = self.main_abc_table[WAREHOUSE_NAME].map(
            self.warehouse_total_with_abc_with_missing_elements.set_index(WAREHOUSE_NAME)[CATEGORY])
        self.main_abc_table['abc_products'] = self.main_abc_table[OFFER_ID].map(
            self.product_total_with_abc_with_missing_elements.set_index(OFFER_ID)[CATEGORY])

        self.main_abc_table.rename(
            columns={WAREHOUSE_NAME: 'warehouse', TITLE: 'product', QUANTITY: 'purchased_product_warehouse',
                     PROCEEDS: 'proceeds_product_warehouse',
                     PROCEEDS_PERCENT: 'proceeds_product_warehouse_percent',
                     CATEGORY: 'abc_product_warehouse'}, inplace=True)

    def create_structure(self):
        self.create_main_table_for_structure()
        self.main_abc_table.drop([ACCUMULATED_PERCENT], axis=1,
                                 inplace=True)  # Здесь потому что это может мне понадобиться
        self.db_abc = []
        for row_index, row in self.main_abc_table.iterrows():
            self.db_abc.append({
                'product': row['product'],
                'warehouse': row['warehouse'],
                'offer_id': row['offer_id'],
                'purchased_product': row['purchased_product'],
                'purchased_product_warehouse': row['purchased_product_warehouse'],
                'purchased_warehouse': row['purchased_warehouse'],
                'proceeds_product': row['proceeds_product'],
                'proceeds_product_warehouse': row['proceeds_product_warehouse'],
                'proceeds_warehouse': row['proceeds_warehouse'],
                'proceeds_product_percent': round(row['proceeds_product_percent'], 1),
                'proceeds_product_warehouse_percent': round(row['proceeds_product_warehouse_percent'], 1),
                'proceeds_warehouse_percent': round(row['proceeds_warehouse_percent'], 1),
                'proceeds_product_accumulated_percent': 0,
                'proceeds_product_warehouse_accumulated_percent':
                    0,
                'proceeds_warehouse_accumulated_percent': 0,
                'abc_products': row['abc_products'],
                'abc_product_warehouse': row['abc_product_warehouse'],
                'abc_warehouse': row['abc_warehouse']
            })

    def run(self):
        self.create_structure()
        return self.db_abc

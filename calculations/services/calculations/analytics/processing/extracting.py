import numpy as np
import pandas as pd
from calculations.services.calculations.analytics.supporting_func.initialization import *
from calculations.services.calculations.supporting.error_processing import *


class V1AnalyticsData:
    list_total_metrics = [METRIC1, METRIC2, METRIC3, METRIC4, METRIC5, METRIC6, METRIC7, METRIC8]
    list_product_metrics = [ID, NAME, METRIC1, METRIC2, METRIC3, METRIC4, METRIC5, METRIC6, METRIC7, METRIC8]

    def __init__(self, data):
        self.data = data

    def get_data(self):
        data = []
        self.time_of_report = self.data[TIMESTAMP]
        self.total_table = pd.Series(self.data[RESULT][TOTALS], index=self.list_total_metrics)
        if not self.data[RESULT][DATA]:
            data = []
            loggers.logger.warning('analytics_data_report is empty')
            raise EmptyData('analytics_data_report is empty')
        for id_product in self.data[RESULT][DATA]:
            id = id_product[DIMENSIONS][0][ID]
            name = id_product[DIMENSIONS][0][NAME]
            metrics = id_product[METRICS]
            product_list = [id, name]
            data_list = product_list + metrics
            data.append(data_list)
        self.product_table = pd.DataFrame(data, columns=self.list_product_metrics)

    def run(self):
        self.get_data()


class V2FinanceTransaction:

    def __init__(self, data):
        self.data = data

    def get_data(self):
        if not self.data[RESULT]:
            self.transaction_table = []
            loggers.logger.warning('finance_transaction_report is empty')
            raise EmptyData('finance_transaction_report is empty')
        self.transaction_table = pd.DataFrame(self.data[RESULT])
        self.transaction_table[TRANDATE] = pd.to_datetime(self.transaction_table[TRANDATE].str[:-10])
        self.transaction_table[ORDERDATE] = pd.to_datetime(self.transaction_table[ORDERDATE])

    def run(self):
        self.get_data()


class V1StockOnWarehouses:

    def __init__(self, data):
        self.data = data

    def get_data(self):
        warehouse_remains_data = []
        total_product_remains_data = []
        if not self.data[WH_ITEMS]:
            self.warehouse_remains_table = []
            loggers.logger.warning('stock_on_warehouses_report is empty')
            raise EmptyData('stock_on_warehouses_report is empty')
        for warehouse in self.data[WH_ITEMS]:
            # warehouse_info = pd.Series({ID: warehouse[ID], NAME: warehouse[NAME]})
            for product in warehouse[ITEMS]:
                warehouse_remains_data.append({ID: warehouse[ID], NAME: warehouse[NAME], OFFER_ID: product[OFFER_ID],
                                               SKU: product[SKU],
                                               TITLE: product[TITLE], LOSS: product[STOCK][LOSS],
                                               FOR_SALE: product[STOCK][FOR_SALE]})
        self.warehouse_remains_table = pd.DataFrame(warehouse_remains_data)
        if not self.data[TOTAL_ITEMS]:
            self.total_product_remains_table = []
            loggers.logger.warning('stock_on_warehouses_report is empty')
            raise EmptyData('stock_on_warehouses_report is empty')
        for product in self.data[TOTAL_ITEMS]:
            total_product_remains_data.append({OFFER_ID: product[OFFER_ID], SKU: product[SKU],
                                               TITLE: product[TITLE], LOSS: product[STOCK][LOSS],
                                               FOR_SALE: product[STOCK][FOR_SALE],
                                               BETWEEN_WAREHOUSES: product[STOCK][BETWEEN_WAREHOUSES],
                                               SHIPPED: product[STOCK][SHIPPED]})
        self.total_product_remains_table = pd.DataFrame(total_product_remains_data)

    def run(self):
        self.get_data()


class V2PostingFbo:

    def __init__(self, data):
        self.data = data

    def get_data(self):
        df_data = []
        if not self.data[RESULT]:
            self.fbo_posting_table = []
            loggers.logger.warning('posting_fbo_report is empty')
            raise EmptyData('posting_fbo_report is empty')
        for order in self.data[RESULT]:
            product_data_with_comission_and_discount = dict()
            product_data_without_comission_and_discount = dict()
            for product in order[PRODUCTS]:
                product_data_without_comission_and_discount[product[SKU]] = {
                    QUANTITY: product[QUANTITY], NAME: product[NAME],
                    OFFER_ID: product[OFFER_ID], PRICE: product[PRICE]}

            for product in order[FINANCIAL_DATA][PRODUCTS]:
                product_data_with_comission_and_discount[product[PRODUCT_ID]] = {SKU: product[PRODUCT_ID],
                                                                                 OLD_PRICE: product[OLD_PRICE],
                                                                                 COMMISSION_PERCENT: product[
                                                                                     COMMISSION_PERCENT],
                                                                                 ORDER_ID: order[ORDER_ID],
                                                                                 IN_PROCESS_AT: order[IN_PROCESS_AT],
                                                                                 REGION: order[ANALYTICS_DATA][REGION],
                                                                                 WAREHOUSE_ID: order[ANALYTICS_DATA][
                                                                                     WAREHOUSE_ID],
                                                                                 WAREHOUSE_NAME: order[ANALYTICS_DATA][
                                                                                     WAREHOUSE_NAME]}

            for key in product_data_with_comission_and_discount.keys():
                merged_dict = {**product_data_with_comission_and_discount[key],
                               **product_data_without_comission_and_discount[key]}
                df_data.append(merged_dict)

        fbo_posting_df = pd.DataFrame(df_data)
        self.fbo_posting_table = fbo_posting_df

    def run(self):
        self.get_data()

from portfolio import Portfolio
import pandas as pd
import itertools
import numpy as np


class Performance:

    def __init__(self) -> None:
        super().__init__()

    def calculate_return(self, port: Portfolio) -> float:
        sum_current = port['current value'].sum()
        sum_buying = port['buy amount'].sum()
        portfolio_return = (sum_current - sum_buying) / sum_buying * 100
        return round(portfolio_return, 2)

    def get_values_for_asset(self, port: Portfolio):
        port_type = ['ST', 'CB', 'PB', 'GO', 'CA']
        values = []

        for asset_type in port_type:
            df_asset = port.get_data_frame_by_asset(asset_type)
            value = df_asset['Price'] * (port[port['asset'] == asset_type]['shares'].iloc[0])
            values.append(pd.Series.sum(value))

        return values

    def calculate_volatility(self, asset_values: list):
        values_series = pd.Series(asset_values)
        std = pd.Series.std(values_series)
        average = pd.Series.mean(values_series)
        return round(std / average * 100, 2)

    def construct_metric(self, port: Portfolio):
        index = pd.concat([pd.Series(port.asset_types), pd.Series(["RETURN", "VOLAT"])])
        df = pd.DataFrame(index=index)
        print(df)

    def generate_portfolios(self):

        df = self.initialize_data_frame()
        self.fill_return_and_volatility(df)

        return df

    def fill_return_and_volatility(self, df):
        for index, row in df.iterrows():
            row = row / 100
            x = Portfolio(['ST', 'CB', 'PB', 'GO', 'CA'], row['ST':'CA'].copy().tolist())
            x.construct_portfolio(100000)

            df.loc[index, 'RETURN'] = self.calculate_return(x)
            df.loc[index, 'VOLAT'] = self.calculate_volatility(self.get_values_for_asset(x))

    def initialize_data_frame(self):
        weights = []
        weight_range = range(0, 105, 20)
        for step in weight_range:
            weights.append(step)
        combinations = list(itertools.product(weights, repeat=5))  # all combinations of weights
        good_allocations = []  # list of allocations that equal to 100
        for i in combinations:
            if sum(i) == 100:
                good_allocations.append(i)
        df = pd.DataFrame(good_allocations, columns=['ST', 'CB', 'PB', 'GO', 'CA'])
        df["RETURN"] = None
        df['VOLAT'] = None
        return df

    def can_add(i, new_list):
        return np.logical_and(new_list[i] > 0, new_list[i] < 100)


performance = Performance()
performance.generate_portfolios().to_csv('portfolio_metrics.csv')

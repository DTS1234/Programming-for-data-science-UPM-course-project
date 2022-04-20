import itertools

import pandas as pd

from Portfolio.portfolio import Portfolio


class Performance:

    def __init__(self) -> None:
        super().__init__()

    def calculate_return(self, port: Portfolio) -> float:
        sum_current = port['current value'].sum()
        sum_buying = port['buy amount'].sum()
        portfolio_return = (sum_current - sum_buying) / sum_buying * 100
        return round(portfolio_return, 2)

    def generate_portfolios(self):

        df = self.initialize_data_frame()
        self.fill_return_and_volatility(df)

        return df

    def fill_return_and_volatility(self, df):
        for index, row in df.iterrows():
            row = row / 100
            portfolio_x = Portfolio(['ST', 'CB', 'PB', 'GO', 'CA'], row['ST':'CA'].copy().tolist())
            portfolio_x.construct_portfolio(1000)

            df.loc[index, 'RETURN'] = self.calculate_return(portfolio_x)
            volatility_portfolio = self.calculate_volatilty(portfolio_x)

            df.loc[index, 'VOLAT'] = volatility_portfolio

    def calculate_volatilty(self, portfolio_x):
        volatilities = []

        for asset in portfolio_x.asset_types:
            prices = portfolio_x.get_data_frame_by_asset(asset)['Price']
            prices_std = pd.Series.std(prices)
            average = pd.Series.mean(prices)
            volatility = prices_std / average * 100
            volatilities.append(volatility)

        final_volat = []

        for i in range(len(portfolio_x.allocation)):
            asset_allocation = portfolio_x.allocation[i]
            final_volat.append(asset_allocation * volatilities[i])

        volatility_portfolio = round(sum(final_volat), 2)

        return volatility_portfolio

    def initialize_data_frame(self):
        df = self.generate_allocations()
        df["RETURN"] = None
        df['VOLAT'] = None
        return df

    def generate_allocations(self):
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
        df.to_csv('portfolio_allocations.csv')

        return df


performance = Performance()
performance.generate_portfolios().to_csv('portfolio_metrics.csv')

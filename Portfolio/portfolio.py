from typing import Any

import pandas as pd


class Portfolio:
    def __init__(self, asset_types: list, allocation: list) -> None:
        super().__init__()
        self.portfolio = None
        self.asset_types = asset_types
        self.check_data(allocation, asset_types)
        self.allocation = allocation

    def check_data(self, allocation, asset_types):
        sum_all = round(sum(allocation), 4)
        if sum_all != 1.0000:
            raise Exception('Allocation must be summing up to 1')
        if len(asset_types) != len(allocation):
            raise Exception('Allocation should be provide for every asset type!')

    def construct_portfolio(self, money) -> pd.DataFrame:

        amounts = []
        prices = []
        shares = []
        buying_prices = []

        for allocation_value in self.allocation:
            amount = money * allocation_value
            amounts.append(amount)

        for asset in self.asset_types:
            price = self.read_current_asset_price(asset)
            prices.append(price)
            buying_price = self.read_buying_asset_price(asset)
            buying_prices.append(buying_price)

        for i in range(len(self.allocation)):
            share = amounts[i] / prices[i]
            shares.append(round(share, 2))

        data = {
            'asset': self.asset_types, 'allocation': self.allocation, 'amount': amounts, 'current price': prices,
            'buying price': buying_prices, 'shares': shares
        }

        self.portfolio = pd.DataFrame(data)
        self.portfolio['buy amount'] = self.portfolio['shares'] * self.portfolio['buying price']
        self.portfolio['current value'] = self.portfolio['shares'] * self.portfolio['current price']

        return self.portfolio

    def read_current_asset_price(self, asset_type):
        data_frame = self.get_data_frame_by_asset(asset_type)

        price_df = data_frame[data_frame['Date'] == 'Dec 31, 2020']['Price']
        if price_df.size == 0:
            price_df = data_frame[data_frame['Date'] == 'Dec 30, 2020']['Price']

        final_price = price_df.iloc[0]

        return final_price

    def read_buying_asset_price(self, asset_type) -> pd.Series:
        data_frame = self.get_data_frame_by_asset(asset_type)

        price_df = data_frame[data_frame['Date'] == 'Jan 01, 2020']['Price']
        if price_df.size == 0:
            price_df = data_frame[data_frame['Date'] == 'Jan 02, 2020']['Price']

        final_price = price_df.iloc[0]

        return final_price

    @staticmethod
    def get_data_frame_by_asset(asset_type) -> pd.DataFrame:
        if asset_type == 'GO':
            data_frame = pd.read_csv('spdr-gold-trust.csv')
        elif asset_type == 'ST':
            data_frame = pd.read_csv('amundi-msci-wrld-ae-c.csv')
        elif asset_type == 'PB':
            data_frame = pd.read_csv('db-x-trackers-ii-global-sovereign-5.csv')
        elif asset_type == 'CA':
            data_frame = pd.read_csv('usdollar.csv')
        elif asset_type == 'CB':
            data_frame = pd.read_csv('ishares-global-corporate-bond-$.csv')
        else:
            raise Exception('No such asset !')

        return data_frame

    def __getitem__(self, item):
        return self.portfolio[item]

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)


p = Portfolio(["ST", "CB", "PB", "GO", "CA"], [0.1, 0.2, 0.4, 0.2, 0.1])
portfolio = p.construct_portfolio(100000)
print(portfolio)

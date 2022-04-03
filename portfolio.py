import pandas as pd


class Portfolio:
    def __init__(self, asset_types: list, allocation: list) -> None:
        super().__init__()
        self.type = asset_types
        self.check_data(allocation, asset_types)
        self.allocation = allocation

    def check_data(self, allocation, asset_types):
        sum_all = round(sum(allocation), 4)
        if sum_all != 1.0000:
            raise Exception('Allocation must be summing up to 1')
        if len(asset_types) != len(allocation):
            raise Exception('Allocation should be provide for every asset type!')

    def construct_portfolio(self, money):

        amounts = []
        prices = []
        shares = []

        for allocation_value in self.allocation:
            amount = money * allocation_value
            amounts.append(amount)

        for asset in self.type:
            price = self.read_asset_price(asset)
            prices.append(price)

        for i in range(len(self.allocation)):
            share = amounts[i] / prices[i]
            shares.append(round(share, 2))

        data = {
            'asset': self.type, 'allocation': self.allocation, 'amount': amounts, 'price': prices, 'shares': shares
        }

        return pd.DataFrame(data)

    def read_asset_price(self, asset_type):
        if asset_type == 'GO':
            data_frame = pd.read_csv('pricedata_Gold.csv')
        elif asset_type == 'ST':
            data_frame = pd.read_csv('pricedata_Stocks.csv')
        elif asset_type == 'PB':
            data_frame = pd.read_csv('pricedata_Public_bonds.csv')
        elif asset_type == 'CA':
            data_frame = pd.read_csv('pricedata_Cash.csv')
        elif asset_type == 'CB':
            data_frame = pd.read_csv('pricedata_Corporate_bonds.csv')
        else:
            raise Exception('No such asset !')

        price_df = data_frame[data_frame['Date'] == 'Dec 31, 2020']['Price']
        if price_df.size == 0:
            price_df = data_frame[data_frame['Date'] == 'Dec 30, 2020']['Price']

        final_price = price_df.iloc[0]

        return final_price


p = Portfolio(["ST", "CB", "PB", "GO", "CA"], [0.1, 0.2, 0.4, 0.2, 0.1])
portfolio = p.construct_portfolio(100000)

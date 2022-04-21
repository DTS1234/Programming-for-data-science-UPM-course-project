import pandas as pd


# this class stores the data about the portfolio structure
class Portfolio:
    def __init__(self, asset_types: list, allocation: list) -> None:
        super().__init__()
        self.portfolio = None
        self.asset_types = asset_types
        self.check_data(allocation, asset_types)
        self.allocation = allocation

    # this class verifies the conditions regarding the allocation values
    @staticmethod
    def check_data(allocation, asset_types):
        sum_all = round(sum(allocation), 4)
        if sum_all != 1.0000:  # must sum to 1
            raise Exception('Allocation must be summing up to 1')
        if len(asset_types) != len(allocation):  # must be provided for every asset type
            raise Exception('Allocation should be provide for every asset type!')

    # this method constructs portfolio object with amounts prices shares and buying price value added
    def construct_portfolio(self, money) -> pd.DataFrame:

        amounts = []
        prices = []
        shares = []
        buying_prices = []

        # creating amount list by multiplying allocation value with money value
        for allocation_value in self.allocation:
            amount = money * allocation_value
            amounts.append(amount)

        # creating prices and buying prices list reading values from the data frames by asset types
        for asset in self.asset_types:
            price = self.read_current_asset_price(asset)
            prices.append(price)
            buying_price = self.read_buying_asset_price(asset)
            buying_prices.append(buying_price)

        # creating shares list by dividing amount by buying price and rounding to two digits after coma
        for i in range(len(self.allocation)):
            share = amounts[i] / buying_prices[i]
            shares.append(round(share, 2))

        # constructing dictionary with column names and lists
        data = {
            'asset': self.asset_types, 'allocation': self.allocation, 'amount': amounts, 'current price': prices,
            'buying price': buying_prices, 'shares': shares
        }

        self.portfolio = pd.DataFrame(data)

        # adding buy amount and current value columns by performing shares multiplication for both prices
        self.portfolio['buy amount'] = self.portfolio['shares'] * self.portfolio['buying price']
        self.portfolio['current value'] = self.portfolio['shares'] * self.portfolio['current price']

        return self.portfolio

    # this method returns the asset price value by asset type given
    def read_current_asset_price(self, asset_type):
        data_frame = self.get_data_frame_by_asset(asset_type)

        price_df = data_frame[data_frame['Date'] == 'Dec 31, 2020']['Price']
        if price_df.size == 0:
            price_df = data_frame[data_frame['Date'] == 'Dec 30, 2020'][
                'Price']  # if there was no data (size == 0) for 31 of December read from 30 of December

        final_price = price_df.iloc[
            0]  # there should be one value only as we specified precise date so we can access the price by index 0

        return final_price

    # this method returns the value of the asset price at the first possible date for given asset
    def read_buying_asset_price(self, asset_type) -> pd.Series:
        data_frame = self.get_data_frame_by_asset(asset_type)

        price_df = data_frame[data_frame['Date'] == 'Jan 01, 2020']['Price']
        if price_df.size == 0:
            price_df = data_frame[data_frame['Date'] == 'Jan 02, 2020'][
                'Price']  # if there was no data (size == 0) for 1 of January read from 2 of January

        final_price = price_df.iloc[
            0]  # there should be one value only as we specified precise date so we can access the price by index 0

        return final_price

    # util function for reading scraped data into data frames based on asset type value
    @staticmethod
    def get_data_frame_by_asset(asset_type) -> pd.DataFrame:
        if asset_type == 'GO':
            data_frame = pd.read_csv('../Scraping/spdr-gold-trust.csv')
        elif asset_type == 'ST':
            data_frame = pd.read_csv('../Scraping/amundi-msci-wrld-ae-c.csv')
        elif asset_type == 'PB':
            data_frame = pd.read_csv('../Scraping/db-x-trackers-ii-global-sovereign-5.csv')
        elif asset_type == 'CA':
            data_frame = pd.read_csv('../Scraping/usdollar.csv')
        elif asset_type == 'CB':
            data_frame = pd.read_csv('../Scraping/ishares-global-corporate-bond-$.csv')
        else:
            raise Exception('No such asset !')

        return data_frame

    # pandas util method to allow other objects to retrieve values
    def __getitem__(self, item):
        return self.portfolio[item]

from portfolio import Portfolio


class Performance:

    def __init__(self) -> None:
        super().__init__()

    def calculate_return(self, port: Portfolio) -> float:
        sum_current = port['current price'].sum()
        sum_buying = port['buying price'].sum()
        portfolio_return = (sum_current - sum_buying) / sum_buying * 100
        return round(portfolio_return, 2)

    def calculate_volatility(self):


        pass


p = Portfolio(["ST", "CB", "PB", "GO", "CA"], [0.1, 0.2, 0.4, 0.2, 0.1])
portfolio = p.construct_portfolio(100000)

performance = Performance()
return_ = performance.calculate_return(p)
print(f'return is {return_}%')

import seaborn as sns
import pandas as pd
import portfolio

p = portfolio.Portfolio(["ST", "CB", "PB", "GO", "CA"], [0.1, 0.2, 0.4, 0.2, 0.1])
p1 = p.construct_portfolio(100000)



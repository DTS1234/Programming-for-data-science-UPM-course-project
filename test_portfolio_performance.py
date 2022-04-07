from unittest import TestCase

import numpy as np

from portfolio_performance import Performance


class TestPerformance(TestCase):
    def test_generate_portfolios(self):
        subject = Performance()
        portfolios = subject.generate_portfolios()
        self.assertEqual(126, np.size(portfolios.index))

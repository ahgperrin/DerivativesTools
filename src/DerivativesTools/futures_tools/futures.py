from datetime import datetime
import numpy as np


class Futures:
    def __init__(self, name: str, maturity: datetime, price: float, qty: float, contract_size: float) -> None:
        self.name = name
        self.maturity = maturity
        self.price = price
        self.qty = qty
        self.contract_size = contract_size

    def remaining_time(self, computation_date: datetime, basis: int) -> float:
        total_year = basis * 86400
        remaining = (self.maturity - computation_date).total_seconds()
        return remaining / total_year

    def implied_rate(self, computation_date: datetime, spot: float, basis: int) -> float:
        return -np.log(spot / self.price) / self.remaining_time(computation_date, basis)

    def contract_value(self) -> float:
        return self.contract_size * self.price

    def hedging_spot(self, position: float) -> float:
        return position / self.contract_value()

    def hedging_portfolio(self, portfolio_size: float, beta: float) -> float:
        return (portfolio_size / self.contract_value()) * beta

    def hedging_cross_asset(self, position: float, sigma_a: float, sigma_fut: float, correlation: float) -> float:
        return correlation * (sigma_a / sigma_fut) * (position / self.contract_value())


class Spot:
    def __init__(self, name: str, price: float, qty: float) -> None:
        self.name = name
        self.price = price
        self.qty = qty

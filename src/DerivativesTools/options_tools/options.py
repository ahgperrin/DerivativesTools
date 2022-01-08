from datetime import datetime


class Options:
    def __init__(self, opt_type: str, price: float, strike: float, side: int, maturity_datetime: datetime,
                 implied_vol: float, risk_free_rate: float, dividend: float,
                 qty: float) -> None:
        self.opt_type = opt_type
        self.strike = strike
        self.price = price
        self.side = side
        self.maturity_datetime = maturity_datetime
        self.implied_vol = implied_vol
        self.risk_free_rate = risk_free_rate
        self.dividend = dividend
        self.qty = qty

    def __repr__(self):
        side = 'long' if self.side == 1 else 'short'
        return f'Option(type={self.opt_type},side={side},strike={self.strike} ,price={self.price})'

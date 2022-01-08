class BsParams:

    def __init__(self, opt_type: str, volatility: float, time_maturity: float, risk_free_rate: float, dividend: float,
                 spot: float, strike: float) -> None:
        self._opt_type = opt_type
        self._volatility = volatility
        self._time_maturity = time_maturity
        self._risk_free_rate = risk_free_rate
        self._dividend = dividend
        self._spot = spot
        self._strike = strike

    @property
    def opt_type(self) -> str:
        return self._opt_type

    @opt_type.setter
    def opt_type(self, opt_type: str) -> None:
        self._opt_type = opt_type

    @property
    def volatility(self) -> float:
        return self._volatility

    @volatility.setter
    def volatility(self, volatility: float) -> None:
        self._volatility = volatility

    @property
    def time_maturity(self) -> float:
        return self._time_maturity

    @time_maturity.setter
    def time_maturity(self, time_maturity: float) -> None:
        self._time_maturity = time_maturity

    @property
    def risk_free_rate(self) -> float:
        return self._risk_free_rate

    @risk_free_rate.setter
    def risk_free_rate(self, risk_free_rate: float) -> None:
        self._risk_free_rate = risk_free_rate

    @property
    def dividend(self) -> float:
        return self._dividend

    @dividend.setter
    def dividend(self, dividend: float) -> None:
        self._dividend = dividend

    @property
    def spot(self) -> float:
        return self._spot

    @spot.setter
    def spot(self, spot: float) -> None:
        self._spot = spot

    @property
    def strike(self) -> float:
        return self._strike

    @strike.setter
    def strike(self, strike: float) -> None:
        self._strike = strike

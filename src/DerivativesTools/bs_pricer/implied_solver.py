from src.DerivativesTools.bs_pricer.pricing import *
import numpy as np


# IMPLIED VOLATILITY SOLVER FUNCTIONS

def implied_vol(params: BsParams, market_quote: float) -> float:
    a = 0
    b = 2
    err_margin = 0.000000000000001
    iv = 0
    current_vol = params.volatility
    error = (b - a) / 2
    while error > err_margin:
        iv = (a + b) / 2
        params.volatility = (a + b) / 2
        if option_price(params) < market_quote:
            a = iv
        else:
            b = iv
        error = (b - a) / 2
    params.volatility = current_vol
    return iv


def volatility_smile(strikes: np.array, prices: np.array, params: BsParams) -> np.array:
    smile = np.zeros(len(strikes))
    for i in range(len(strikes)):
        params.strike = strikes[i]
        iv = implied_vol(params, prices[i])
        smile[i] = iv
    return smile


def volatility_surface(strikes: np.array, times: np.array, prices: np.array, params: BsParams) -> np.array:
    surface = np.zeros((len(strikes), len(times)))
    for i in range(len(strikes)):
        params.strike = strikes[i]
        for j in range(len(times)):
            params.time_maturity = times[j]
            surface[i][j] = implied_vol(params, prices[i][j])
    return surface

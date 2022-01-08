from scipy.stats import norm
from scipy.optimize import minimize_scalar
import numpy as np
import pandas as pd


def european_call(spot: float, strike: float, sigma: float, mu: float, tt_maturity: float) -> float:
    discount = np.exp(-mu * tt_maturity)
    volat_mod = sigma * np.sqrt(tt_maturity)
    moneyness = np.log(spot / strike)
    term_vol = (mu + 0.5 * sigma ** 2) * tt_maturity
    return spot * norm.cdf((moneyness + term_vol) / volat_mod) - discount * \
           strike * norm.cdf(((moneyness + term_vol) / volat_mod) - volat_mod)


def european_put(spot: float, strike: float, sigma: float, mu: float, tt_maturity: float) -> float:
    discount = np.exp(-mu * tt_maturity)
    volat_mod = sigma * np.sqrt(tt_maturity)
    moneyness = np.log(spot / strike)
    term_vol = (mu + 0.5 * sigma ** 2) * tt_maturity
    d1 = (moneyness + term_vol) / volat_mod
    d2 = d1 - volat_mod
    return - (spot * norm.cdf(-d1) - discount * strike * norm.cdf(-d2))


def implied_volatility_call(spot: float, strike: float, mu: float, tt_maturity: float,
                            price: float) -> float:
    def call(sigma: float) -> float:
        return np.power(european_call(spot, strike, sigma, mu, tt_maturity) - price, 2)

    res = minimize_scalar(call, bounds=(0.01, 6), method='bounded')
    return res.x


def implied_volatility_put(spot: float, strike: float, mu: float, tt_maturity: float,
                           price: float) -> float:
    def put(sigma: float) -> float:
        return np.power(european_put(spot, strike, sigma, mu, tt_maturity) - price, 2)

    res = minimize_scalar(put, bounds=(0.01, 6), method='bounded')
    return res.x


def volatility_smile_call(market_data: pd.DataFrame, spot: float, mu: float, tt_maturity: float) -> list:
    smile = []
    for row in market_data.itertuples():
        smile.append(implied_volatility_call(spot, row.strike, mu, tt_maturity, row.call))
    return smile


def volatility_smile_put(market_data: pd.DataFrame, spot: float, mu: float, tt_maturity: float) -> list:
    smile = []
    for row in market_data.itertuples():
        smile.append(implied_volatility_put(spot, row.strike, mu, tt_maturity, row.put))
    return smile

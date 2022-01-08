from src.DerivativesTools.bs_pricer.bs_params import BsParams
from scipy.stats import norm
import numpy as np


def moneyness(params: BsParams) -> float:
    return params.spot / params.strike


def vol_term(params: BsParams) -> float:
    return params.volatility * np.sqrt(params.time_maturity)


def drift(params: BsParams) -> float:
    return (params.risk_free_rate - params.dividend + (np.power(params.volatility, 2.00) / 2)) * params.time_maturity


def d1(params: BsParams) -> float:
    return (np.log(moneyness(params)) + drift(params)) / vol_term(params)


def d2(params: BsParams) -> float:
    return d1(params) - vol_term(params)


def discount_factor(params: BsParams) -> float:
    return np.exp(-params.risk_free_rate * params.time_maturity)


def dividend_factor(params: BsParams) -> float:
    return np.exp(-params.dividend * params.time_maturity)


def option_price(params: BsParams) -> float:
    if params.opt_type == "c":
        spot_part = params.spot * norm.cdf(d1(params)) * dividend_factor(params)
        strike_part = params.strike * norm.cdf(d2(params)) * discount_factor(params)
        return spot_part - strike_part
    else:
        spot_part = params.spot * norm.cdf(-d1(params)) * dividend_factor(params)
        strike_part = params.strike * norm.cdf(-d2(params)) * discount_factor(params)
        return strike_part - spot_part

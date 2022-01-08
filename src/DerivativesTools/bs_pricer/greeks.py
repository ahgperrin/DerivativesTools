import numpy as np
from src.DerivativesTools.bs_pricer.pricing import *
from scipy.stats import norm


# GREEKS SENSIBILITY FUNCTIONS

# First order greeks

def rho(params: BsParams, side: int) -> float:
    if params.opt_type == "c'":
        return 0.01 * side * discount_factor(params) * params.time_maturity * params.strike * norm.cdf(d2(params))
    return 0.01 * side * -discount_factor(params) * params.time_maturity * params.strike * norm.cdf(-d2(params))


def vega(params: BsParams, side: int) -> float:
    return side * 0.01 * params.spot * dividend_factor(params) * np.sqrt(params.time_maturity * norm.pdf(d1(params)))


def theta(params: BsParams, side: int) -> float:
    term_1 = -dividend_factor(params) * (
                ((params.spot * norm.pdf(d1(params))) * params.volatility) / (2 * np.sqrt(params.time_maturity)))
    term_2 = params.risk_free_rate * params.strike * discount_factor(params)
    term_3 = params.dividend * params.spot * dividend_factor(params)
    if params.opt_type == "c":
        return side * (term_1 - term_2 * norm.cdf(d2(params)) + term_3 * norm.cdf(d1(params))) / 365
    else:
        return side * (term_1 + term_2 * norm.cdf(-d2(params)) - term_3 * norm.cdf(-d1(params))) / 365


def delta(params: BsParams, side: int) -> float:
    if params.opt_type == "c":
        return side * (dividend_factor(params) * norm.cdf(d1(params)))
    else:
        return side * (-dividend_factor(params) * norm.cdf(-d1(params)))


def omega(params: BsParams, side: int) -> float:
    return delta(params, side) * (params.spot / option_price(params))


# Second order greeks

def gamma(params: BsParams, side: int) -> float:
    return side * dividend_factor(params) * (norm.pdf(d1(params)) / (params.spot * vol_term(params)))


def vanna(params: BsParams, side: int) -> float:
    return side * 0.01 * (-dividend_factor(params) * (norm.pdf(d1(params))) * (d2(params) / params.volatility))


def vomma(params: BsParams, side: int) -> float:
    return side * 0.01 * vega(params, 1) * ((d1(params) * d2(params)) / params.volatility)


def option_carac(params: BsParams, side: int) -> dict:
    return {
        "Price": option_price(params),
        "Volatility": params.volatility,
        "Delta": delta(params, side),
        "Vega": vega(params, side),
        "Rho": rho(params, side),
        "Theta": theta(params, side),
        "Omega": omega(params, side),
        "Gamma": gamma(params, side),
        "Vanna": vanna(params, side),
        "Vomma": vomma(params, side),

    }

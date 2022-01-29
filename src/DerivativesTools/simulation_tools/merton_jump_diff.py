import numpy as np
import pandas as pd
from scipy.optimize import minimize
from DerivativesTools.simulation_tools.model_params import JumpDiffusionParams
from DerivativesTools.simulation_tools.simulation_computation import Simulation
from DerivativesTools.simulation_tools.tools import european_call, european_put
from DerivativesTools.options_tools.vol_structure import SmileView
from DerivativesTools.bs_pricer.implied_solver import *


def merton_jump_path(mjd_params: JumpDiffusionParams, n_paths: int) -> Simulation:
    poi_rv = np.multiply(np.random.poisson(mjd_params.j_lambda * (mjd_params.tt_maturity / mjd_params.delta),
                                           size=(mjd_params.delta - 1, n_paths)),
                         np.random.normal(mjd_params.j_mu, mjd_params.j_sigma,
                                          size=(mjd_params.delta - 1, n_paths))).cumsum(axis=0)
    geo = np.cumsum(((mjd_params.mu - mjd_params.sigma ** 2 / 2 - mjd_params.j_lambda * (
            mjd_params.j_mu + mjd_params.j_sigma ** 2 * 0.5)) * (mjd_params.tt_maturity / mjd_params.delta) +
                     mjd_params.sigma * np.sqrt((mjd_params.tt_maturity / mjd_params.delta)) *
                     np.random.normal(size=(mjd_params.delta - 1, n_paths))), axis=0)

    return Simulation(np.insert(np.exp(geo + poi_rv) * mjd_params.spot_zero, 0, mjd_params.spot_zero, axis=0))


def merton_jump_call(mjd_params: JumpDiffusionParams, strike: float):
    price = 0
    mu = np.exp(mjd_params.j_mu + mjd_params.j_sigma ** 2 * 0.5)
    for k in range(40):
        cum_rate = mjd_params.mu - mjd_params.j_lambda * (mu - 1) + \
                   (k * np.log(mu)) / mjd_params.tt_maturity
        cum_sigma = np.sqrt(mjd_params.sigma ** 2 + (k * mjd_params.j_sigma ** 2) / mjd_params.tt_maturity)
        k_fact = np.math.factorial(k)
        bs_call = european_call(mjd_params.spot_zero, strike, cum_sigma, cum_rate, mjd_params.tt_maturity)
        price += (np.exp(-mu * mjd_params.j_lambda * mjd_params.tt_maturity) *
                  (mu * mjd_params.j_lambda * mjd_params.tt_maturity) ** k / k_fact) * bs_call
    return price


def merton_jump_put(mjd_params: JumpDiffusionParams, strike: float):
    price = 0
    mu = np.exp(mjd_params.j_mu + mjd_params.j_sigma ** 2 * 0.5)
    for k in range(40):
        cum_rate = mjd_params.mu - mjd_params.j_lambda * (mu - 1) + (k * np.log(mu)) / mjd_params.tt_maturity
        cum_sigma = np.sqrt(mjd_params.sigma ** 2 + (k * mjd_params.j_sigma ** 2) / mjd_params.tt_maturity)
        k_fact = np.math.factorial(k)
        bs_put = european_put(mjd_params.spot_zero, strike, cum_sigma, cum_rate, mjd_params.tt_maturity)
        price += (np.exp(-mu * mjd_params.j_lambda * mjd_params.tt_maturity) *
                  (mu * mjd_params.j_lambda * mjd_params.tt_maturity) ** k / k_fact) * bs_put
    return price


def merton_jump_histo_calibration(mjd_params: JumpDiffusionParams, returns: pd.Series, base,
                                  jumps: float, nb_days: int) -> JumpDiffusionParams:
    jumps_values = returns[(returns >= jumps) | (returns <= -jumps)].dropna()
    mjd_params.j_lambda = len(jumps_values) / len(returns)
    mjd_params.j_sigma = float(jumps_values.std())
    mjd_params.j_mu = float(jumps_values.mean())
    returns = returns[~((returns >= jumps) | (returns <= -jumps))]
    mjd_params.mu = float(returns.tail(nb_days).dropna().mean() * base)
    mjd_params.sigma = float(returns.tail(nb_days).dropna().std() * np.sqrt(base))
    return mjd_params


def squared_error_function(x: list, mkt_prices: list, strikes: list, spot: float, tt_maturity: float, delta: int,
                           optype: str):
    candidate_prices = []
    for strike in strikes:
        mjd_params = JumpDiffusionParams(mu=x[0], sigma=x[1], tt_maturity=tt_maturity, delta=delta, spot_zero=spot,
                                         jumps_lambda=x[2], jumps_mu=x[3], jumps_sigma=x[4])
        if optype == "c":
            candidate_prices.append(merton_jump_call(mjd_params, strike))
        elif optype == "p":
            candidate_prices.append(merton_jump_put(mjd_params, strike))
    return np.linalg.norm(np.array(mkt_prices) - np.array(candidate_prices), 2)


def calibrate(mkt_prices, strikes, spot, tt_maturity, delta, optype: str):
    x0 = [0.0001, 0.0001, 0.5, 0.0001, 0.2]
    bounds = ((0.0, np.inf), (0.01, np.inf), (0.01, 2), (1e-5, np.inf), (0, 5))
    res = minimize(squared_error_function, method='SLSQP', x0=x0, args=(mkt_prices, strikes, spot, tt_maturity, delta,optype),
                   bounds=bounds, tol=1e-20,
                   options={"maxiter": 1000})
    return res

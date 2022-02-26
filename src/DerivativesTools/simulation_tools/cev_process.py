from DerivativesTools.simulation_tools.model_params import ConstantElasticityParams
from DerivativesTools.simulation_tools.simulation_computation import Simulation
import numpy as np


def constant_elasticity_path(cev_params: ConstantElasticityParams, n_paths: int) -> Simulation:
    gaussian_increments = np.random.normal(size=(cev_params.delta - 1, n_paths))
    res = np.zeros(shape=(cev_params.delta, n_paths))
    res[0] = 1
    sqrt_dt = np.sqrt(cev_params.tt_maturity / cev_params.delta)
    for i in range(cev_params.delta - 1):
        res[i + 1] = res[i] + res[i] * cev_params.mu * (
                cev_params.tt_maturity / cev_params.delta) + cev_params.sigma * (res[i] ** cev_params.gamma) * \
                     gaussian_increments[i] * sqrt_dt
    return Simulation(res * cev_params.spot_zero)


def log_increment(histo: np.array) -> np.array:
    return np.diff(histo) / histo[:-1]


def historical_calibration(cev_params: ConstantElasticityParams, histo_price: np.array,
                           histo_depth: int, mu: bool = True) -> ConstantElasticityParams:
    histo_price = histo_price[-histo_depth:]
    log_returns = log_increment(histo_price)
    alpha = -10
    mod_increments = (log_increment(histo_price ** (1 + alpha)) / (1 + alpha))
    center = 2 * (mod_increments - log_returns) / (alpha * (cev_params.tt_maturity/cev_params.delta))
    log_center = np.log(center)
    log_price = np.log(histo_price[:-1])

    ones = np.ones(histo_price[:-1].shape[0])
    a = np.column_stack((ones, log_price))

    res = np.linalg.lstsq(a, log_center, rcond=None)[0]
    cev_params.sigma = 2 * np.exp(res[0] / 2)
    cev_params.gamma = 0.5 * (res[1] + 2)
    if mu:
        cev_params.mu = np.mean(log_returns) * cev_params.delta
    else:
        cev_params.mu = 0
    return cev_params

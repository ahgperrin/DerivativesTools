import arch
import numpy as np
import pandas as pd
from DerivativesTools.simulation_tools.model_params import HestonParams, OrnsteinUhlenbeckParams
from DerivativesTools.simulation_tools.ornstein_uhlenbeck import calibration_ornstein_uhlenbeck
from DerivativesTools.simulation_tools.simulation_computation import Simulation, SimulationProcVol

pd.options.mode.chained_assignment = None


def covariance_matrix(heston_params: HestonParams):
    return np.array([0, 0]), np.array([[1, heston_params.covariance], [heston_params.covariance, 1]])


def correlated_wiener(heston_params: HestonParams, n_path: int):
    return np.random.multivariate_normal(covariance_matrix(heston_params)[0], covariance_matrix(heston_params)[1],
                                         size=n_path)


def heston_path(heston_params: HestonParams, n_paths: int, volat_process: bool = False):
    delta_t = heston_params.tt_maturity / heston_params.delta
    prices = np.zeros(shape=(n_paths, heston_params.delta))
    volatility = np.zeros(shape=(n_paths, heston_params.delta))
    exp_factor = np.exp(- heston_params.alpha * (heston_params.tt_maturity / heston_params.delta))
    double_exp_factor = np.exp(- 2 * heston_params.alpha * (heston_params.tt_maturity / heston_params.delta))
    spot_euler = heston_params.spot_zero
    vol_euler = heston_params.vol_zero
    for time in range(heston_params.delta):
        wiener_correlated = correlated_wiener(heston_params, n_paths)
        spot_euler = spot_euler * (np.exp((heston_params.mu - 0.5 * vol_euler) *
                                          delta_t + np.sqrt(vol_euler) * wiener_correlated[:, 0] * np.sqrt(delta_t)))
        vol_euler = np.abs(vol_euler * exp_factor + heston_params.mu_vol * (1 - exp_factor) +
                           heston_params.sigma_vol * np.sqrt((1 - double_exp_factor) / 2 * heston_params.alpha)
                           * wiener_correlated[:, 1])
        prices[:, time] = spot_euler
        volatility[:, time] = vol_euler
    prices = np.insert(prices.T, 0, heston_params.spot_zero, axis=0)
    volatility = np.insert(volatility.T, 0, heston_params.vol_zero, axis=0)
    if volat_process:
        return SimulationProcVol(prices, volatility)
    return Simulation(prices)


def heston_histo_calibration(heston_params: HestonParams, data: pd.Series, base):
    returns = (np.log(data) - np.log(data.shift(1))) * 100
    returns = returns.dropna()
    vol_estimation = arch.arch_model(returns, p=1, o=0, q=1)
    res = vol_estimation.fit(update_freq=5, disp="off")
    cond_vol = (res.conditional_volatility * np.sqrt(base)) / 100
    params_ou = OrnsteinUhlenbeckParams(kappa=heston_params.alpha, tt_maturity=heston_params.tt_maturity,
                                        delta=heston_params.delta, spot_zero=heston_params.vol_zero,
                                        theta=heston_params.mu_vol, sigma=heston_params.sigma_vol)
    params_ou = calibration_ornstein_uhlenbeck(params_ou, cond_vol)[0]
    heston_params.covariance = np.corrcoef(np.array(data.tail(len(data) - 1)).flatten(),
                                           np.array(cond_vol).flatten())[0, 1]
    heston_params.mu = float(returns.mean() / 100 * base)
    heston_params.sigma_vol = params_ou.sigma
    heston_params.mu_vol = params_ou.theta
    heston_params.alpha = params_ou.kappa
    return heston_params

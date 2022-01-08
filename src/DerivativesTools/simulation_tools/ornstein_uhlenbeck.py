from src.DerivativesTools.simulation_tools.model_params import OrnsteinUhlenbeckParams
import numpy as np
import pandas as pd
from src.DerivativesTools.simulation_tools.simulation_computation import Simulation
from sklearn.linear_model import LinearRegression


def ornstein_uhlenbeck_path(ou_params: OrnsteinUhlenbeckParams, n_paths: int) -> Simulation:
    ou_process = np.insert(np.zeros(shape=(ou_params.delta - 1, n_paths)), 0, ou_params.spot_zero, axis=0)
    exp_factor = np.exp(-ou_params.kappa * (ou_params.tt_maturity / ou_params.delta))
    double_exp_factor = np.exp(- 2 * ou_params.kappa * (ou_params.tt_maturity / ou_params.delta))
    for t in range(1, ou_params.delta, 1):
        ou_process[t] = ou_process[t - 1] * exp_factor + ou_params.theta * (1 - exp_factor) + \
                        ou_params.sigma * np.sqrt((1 - double_exp_factor) / 2 * ou_params.kappa) * np.random.normal(
            size=(1, n_paths))
    return Simulation(ou_process)


def calibration_ornstein_uhlenbeck(ou_params: OrnsteinUhlenbeckParams,
                                   asset_price: pd.Series) -> tuple:
    shifted_data = asset_price.shift(1).dropna()
    data = asset_price.tail(n=len(asset_price) - 1)
    x = np.array(data.values).reshape((-1, 1))
    y = np.array(shifted_data.values)
    linear_model = LinearRegression().fit(x, y)

    linear_model_result = {
        "alpha": float(linear_model.intercept_),
        "beta": float(linear_model.coef_),
        "r_2": linear_model.score(x, y)
    }
    estimated = linear_model.predict(np.array(data.values).reshape((-1, 1)))
    squared_error = (data - estimated) ** 2
    linear_model_result["s_error"] = float(np.sqrt(np.sum(squared_error) / (data.count() - 3)))
    delta_t = ou_params.tt_maturity / ou_params.delta
    numer = -2 * np.log(linear_model_result.get("beta"))
    denom = (1 - linear_model_result.get("beta") ** 2) * delta_t
    ou_params.kappa = -(np.log(linear_model_result.get("beta")) / delta_t)
    ou_params.theta = linear_model_result.get("alpha") / (1 - linear_model_result.get("beta"))
    ou_params.sigma = linear_model_result.get("s_error") * np.sqrt(numer / denom)
    ou_params.print_model()
    return ou_params, linear_model_result

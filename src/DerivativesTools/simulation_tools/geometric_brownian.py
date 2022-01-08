from src.DerivativesTools.simulation_tools.model_params import GeometricBrownianParams
import numpy as np
import pandas as pd
from typing import Union

from src.DerivativesTools.simulation_tools.simulation_computation import Simulation


def brownian_path(geo_params: GeometricBrownianParams, n_paths: int) -> Simulation:
    return Simulation(np.insert(np.exp(np.cumsum(((geo_params.mu - geo_params.sigma ** 2 / 2) *
                                                  (geo_params.tt_maturity / geo_params.delta) + geo_params.sigma *
                                                  np.sqrt(geo_params.tt_maturity / geo_params.delta) *
                                                  np.random.normal(size=(geo_params.delta - 1, n_paths))), axis=0)) *
                                geo_params.spot_zero, 0, geo_params.spot_zero, axis=0))


def brownian_path_wiener(geo_params: GeometricBrownianParams, wiener: np.ndarray) -> Simulation:
    return Simulation(np.insert(np.exp(np.cumsum(((geo_params.mu - geo_params.sigma ** 2 / 2) *
                                                  (geo_params.tt_maturity / geo_params.delta) + geo_params.sigma *
                                                  np.sqrt(geo_params.tt_maturity / geo_params.delta) *
                                                  wiener), axis=0)) *
                                geo_params.spot_zero, 0, geo_params.spot_zero, axis=0))


def brownian_histo_calibration(geo_params: GeometricBrownianParams, returns: Union[np.ndarray, pd.Series],
                               base) -> GeometricBrownianParams:
    geo_params.mu = returns.dropna().mean() * base
    geo_params.sigma = returns.dropna().std() * np.sqrt(base)
    geo_params.delta = base
    return geo_params

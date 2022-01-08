import numpy as np

from src.DerivativesTools.simulation_tools.geometric_brownian import brownian_path_wiener
from src.DerivativesTools.simulation_tools.model_params import GeometricBrownianParams
from src.DerivativesTools.simulation_tools.simulation_computation import Simulation


def create_matrix(returns_matrix: np.ndarray):
    matrix = np.corrcoef(returns_matrix, rowvar=False)
    return matrix, [0 for _ in range(len(matrix))]


def correlated_wiener(matrix, mu_matrix, n_path: int):
    return np.random.multivariate_normal(mu_matrix, matrix,
                                         size=n_path)


def correlated_brownian(matrix, mu_matrix, list_params: list[GeometricBrownianParams], weights: list) -> np.ndarray:
    wiener = correlated_wiener(matrix, mu_matrix, list_params[0].delta - 1)
    paths = np.ndarray(shape=(len(matrix), list_params[0].delta))
    for i in range(len(mu_matrix)):
        paths[i] = brownian_path_wiener(list_params[i], wiener[:, i]).paths * weights[i]
    return paths.T


def portfolio_paths(matrix, mu_matrix, list_params: list[GeometricBrownianParams], weights: list,
                    nb_paths: int) -> Simulation:
    paths = np.ndarray(shape=(nb_paths, list_params[0].delta))
    for i in range(nb_paths):
        paths[i] = np.sum(correlated_brownian(matrix, mu_matrix, list_params, weights), axis=1)
    return Simulation(paths.T)

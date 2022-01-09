import numpy as np
import pandas as pd
import scipy.stats as st
import math
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import scipy.stats as stats
import statsmodels.api as sm
import pylab as py
plt.style.use("seaborn")


class Simulation:

    def __init__(self, paths: np.ndarray) -> None:
        self._paths = paths


    @property
    def paths(self) -> np.ndarray:
        return self._paths

    @paths.setter
    def paths(self, paths) -> None:
        self._paths = paths

    def plot_simulation(self, title: str, nb_paths: int) -> plt.Figure:
        fig = plt.figure()
        fig.suptitle(title)
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.plot(self.paths[:, [i for i in range(nb_paths)]], lw=0.7)
        ax1.set_xlabel("Time,t")
        ax1.set_ylabel("Asset Price")
        plt.show()
        return fig

    def european_call(self, strike: float, rf: float, tt_maturity: float) -> float:
        return np.mean(np.maximum(self.paths[-1] - strike, 0)) * np.exp(-rf * tt_maturity)

    def european_put(self, strike: float, rf: float, tt_maturity: float) -> float:
        return np.mean(strike - np.maximum(self.paths[-1], 0)) * np.exp(-rf * tt_maturity)

    def value_at_risk(self, alpha: float):
        nb_scenarios = math.ceil(alpha * len(self.paths[0]))
        sorted_scenarios = np.sort(self.paths[-1])
        var = sorted_scenarios[nb_scenarios] - self.paths[0, 0]
        conf_int = st.t.interval(1 - alpha, len(sorted_scenarios) - 1, loc=var, scale=st.sem(sorted_scenarios))
        return var, conf_int

    def plot_distribution(self):
        df = pd.DataFrame(self.paths)
        ret = np.log(df) - np.log(df.shift(1).dropna())
        fig = plt.figure(figsize=(10, 7))
        fig.suptitle("Distribution Against normal distribution")
        ax1 = plt.subplot2grid((2, 1), (0, 0), rowspan=1, colspan=1, fig=fig)
        sns.distplot(ret.dropna(), fit=norm, ax=ax1)
        ax2 = plt.subplot2grid((2, 1), (1, 0), rowspan=1, colspan=1, fig=fig)
        sm.qqplot(ret.dropna().values.flatten(), line='q',ax=ax2)
        py.show()


class SimulationProcVol:

    def __init__(self, paths: np.ndarray, paths_vol: np.ndarray) -> None:
        self._paths = paths
        self._paths_vol = paths_vol

    @property
    def paths(self) -> np.ndarray:
        return self._paths

    @paths.setter
    def paths(self, paths) -> None:
        self._paths = paths

    @property
    def paths_vol(self) -> np.ndarray:
        return self._paths_vol

    @paths_vol.setter
    def paths_vol(self, paths_vol) -> None:
        self._paths_vol = paths_vol

    def european_call(self, strike: float, rf: float, tt_maturity: float) -> float:
        return np.mean(np.maximum(self.paths[-1] - strike, 0)) * np.exp(-rf * tt_maturity)

    def european_put(self, strike: float, rf: float, tt_maturity: float) -> float:
        return np.mean(strike - np.maximum(self.paths[-1], 0)) * np.exp(-rf * tt_maturity)

    def value_at_risk(self, alpha: float):
        nb_scenarios = math.ceil(alpha * len(self.paths[0]))
        sorted_scenarios = np.sort(self.paths[-1])
        var = sorted_scenarios[nb_scenarios] - self.paths[0, 0]
        conf_int = st.t.interval(1 - alpha, len(sorted_scenarios) - 1, loc=var, scale=st.sem(sorted_scenarios))
        return var, conf_int

    def plot_simulation(self, title: str, nb_paths: int) -> plt.Figure:
        fig = plt.figure()
        fig.suptitle(title)
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.plot(self.paths[:, [i for i in range(nb_paths)]], lw=0.7)
        ax1.set_xlabel("Time,t")
        ax1.set_ylabel("Asset Price")
        return fig

    def plot_volatility(self, title: str, nb_paths: int) -> plt.Figure:
        fig = plt.figure()
        fig.suptitle(title)
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.plot(self.paths_vol[:, [i for i in range(nb_paths)]], lw=0.7)
        ax1.set_xlabel("Time,t")
        ax1.set_ylabel("Asset Volatility")
        return fig

    def plot_both(self, title: str, nb_paths: int) -> plt.Figure:
        fig = plt.figure()
        fig.suptitle(title)
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(self.paths[:, [i for i in range(nb_paths)]], lw=0.7)
        ax1.set_xlabel("Time,t")
        ax1.set_ylabel("Asset Price")
        ax2 = fig.add_subplot(2, 1, 2)
        ax2.plot(self.paths_vol[:, [i for i in range(nb_paths)]], lw=0.7)
        ax2.set_xlabel("Time,t")
        ax2.set_ylabel("Asset Volatility")
        return fig

    def plot_distribution(self):
        df = pd.DataFrame(self.paths)
        ret = np.log(df) - np.log(df.shift(1).dropna())
        fig = plt.figure(figsize=(10, 7))
        fig.suptitle("Distribution Against normal distribution")
        ax1 = plt.subplot2grid((2, 1), (0, 0), rowspan=1, colspan=1, fig=fig)
        sns.distplot(ret.dropna(), fit=norm, ax=ax1)
        ax2 = plt.subplot2grid((2, 1), (1, 0), rowspan=1, colspan=1, fig=fig)
        sm.qqplot(ret.dropna().values.flatten(), line='q',ax=ax2)
        py.show()
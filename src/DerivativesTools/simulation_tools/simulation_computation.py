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
from scipy.interpolate import interp1d

plt.style.use("seaborn")


class Simulation:

    def __init__(self, paths: np.ndarray, paths_vol=None) -> None:
        self._paths = paths
        self._paths_vol = paths_vol
        self._var_paths = self.var_function(0.01, True)
        self._var_up_paths = self.var_function(0.01, False)
        self._vol_var_paths = self.vol_var_function(0.01, True)
        self._vol_var_up_paths = self.vol_var_function(0.01, False)

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

    @property
    def var_paths(self) -> list:
        return self._var_paths

    @var_paths.setter
    def var_paths(self, var_paths: tuple) -> None:
        self._var_paths = var_paths

    @property
    def var_up_paths(self) -> list:
        return self._var_up_paths

    @var_up_paths.setter
    def var_up_paths(self, var_up_paths: tuple) -> None:
        self._var_up_paths = var_up_paths

    @property
    def vol_var_paths(self) -> list:
        return self._vol_var_paths

    @vol_var_paths.setter
    def vol_var_paths(self, vol_var_paths: tuple) -> None:
        self._vol_var_paths = vol_var_paths

    @property
    def vol_var_up_paths(self) -> list:
        return self._vol_var_up_paths

    @vol_var_up_paths.setter
    def vol_var_up_paths(self, vol_var_up_paths: tuple) -> None:
        self._vol_var_up_paths = vol_var_up_paths

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
        return np.mean(np.maximum(strike - self.paths[-1], 0)) * np.exp(-rf * tt_maturity)

    def value_at_risk(self, alpha: float, up: bool = True):
        nb_scenarios = math.ceil(alpha * len(self.paths[0]))
        if up:
            sorted_scenarios = np.sort(self.paths[-1])
            var = sorted_scenarios[nb_scenarios] - self.paths[0, 0]
        else:
            sorted_scenarios = np.sort(self.paths[-1])[::-1]
            var = self.paths[0, 0] - sorted_scenarios[nb_scenarios]
        conf_int = st.t.interval(1 - alpha, len(sorted_scenarios) - 1, loc=var, scale=st.sem(sorted_scenarios))
        return var, conf_int

    def vol_var_function(self, alpha: float, up: bool = True):
        nb_scenarios = math.ceil(alpha * len(self.paths_vol[0]))
        var = []
        for i in range(len(self.paths_vol)):
            if up:
                sorted_scenarios = np.sort(self.paths_vol[i])
                var.append(sorted_scenarios[nb_scenarios] )
            else:
                sorted_scenarios = np.sort(self.paths_vol[i])[::-1]
                var.append(sorted_scenarios[nb_scenarios])
        return var

    def var_function(self, alpha: float, up: bool = True):
        nb_scenarios = math.ceil(alpha * len(self.paths[0]))
        var = []
        for i in range(len(self.paths)):
            if up:
                sorted_scenarios = np.sort(self.paths[i])
                var.append(sorted_scenarios[nb_scenarios] - self.paths[0, 0])
            else:
                sorted_scenarios = np.sort(self.paths[i])[::-1]
                var.append(self.paths[0, 0] - sorted_scenarios[nb_scenarios])
        return var

    def interpolate_var(self, time_var: float, up: bool = True):
        if up:
            var_interp = interp1d(np.arange(0, len(self.var_paths), 1), self.var_paths, kind='cubic')
        else:
            var_interp = interp1d(np.arange(0, len(self.var_up_paths), 1), self.var_up_paths, kind='cubic')
        return float(var_interp(time_var))

    def interpolate_var_vol(self, time_var: float, up: bool = True):
        if up:
            var_interp = interp1d(np.arange(0, len(self.vol_var_paths), 1), self.vol_var_paths, kind='cubic')
        else:
            var_interp = interp1d(np.arange(0, len(self.vol_var_up_paths), 1), self.vol_var_up_paths, kind='cubic')
        return float(var_interp(time_var))

    def plot_var(self, up: bool = True):
        if up:
            var = self.var_paths
        else:
            var = self.var_up_paths
        fig = plt.figure()
        fig.suptitle("Value at risk function")
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.plot(var, lw=0.7)
        ax1.set_xlabel("Time,t")
        ax1.set_ylabel("Value at risk "+str(0.01*100)+"%")

    def breakeven_probability(self, breakeven_value: float):
        sorted_scenarios = np.sort(self.paths[-1])
        filter_scenario = sorted_scenarios[sorted_scenarios > breakeven_value]
        return len(filter_scenario) / len(sorted_scenarios)

    def breakeven_monte_carlo(self, breakeven_vals: []):
        probs = []
        for born in breakeven_vals:
            probs.append(self.breakeven_probability(born))
        return probs

    def plot_volatility(self, title: str, nb_paths: int) -> plt.Figure:
        if self.paths_vol is None:
            raise Exception("Not available with constant volatility")
        fig = plt.figure()
        fig.suptitle(title)
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.plot(self.paths_vol[:, [i for i in range(nb_paths)]], lw=0.7)
        ax1.set_xlabel("Time,t")
        ax1.set_ylabel("Asset Volatility")
        return fig

    def plot_both(self, title: str, nb_paths: int) -> plt.Figure:
        if self.paths_vol is None:
            raise Exception("Not available with constant volatility")
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
        sm.qqplot(ret.dropna().values.flatten(), line='q', ax=ax2)
        py.show()

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import interp1d, griddata
import numpy as np

plt.style.use('bmh')


class Smile:
    def __init__(self, strikes: np.array, vols: np.array) -> None:
        self._strikes = strikes
        self._vols = vols

    @property
    def strikes(self) -> np.array:
        return self._strikes

    @property
    def vols(self) -> np.array:
        return self._vols


class SmileView(Smile):
    def __init__(self, strikes: np.array, implied_vols: np.array) -> None:
        super(SmileView, self).__init__(strikes, implied_vols)

    def get_volatility(self, strike: float) -> float:
        smile_interp = interp1d(self.strikes, self.vols, kind='cubic')
        return float(smile_interp(strike))

    def plot_smile(self) -> plt.figure:
        fig = plt.figure(figsize=(12.5, 8))
        ax1 = fig.add_subplot(111)
        ax1.set_xlabel("Strikes")
        ax1.set_ylabel('IV (%)')
        strikes = np.arange(self.strikes[0], self.strikes[len(self.strikes) - 1], self.strikes[0] / 1000)
        vols = np.zeros(len(strikes))
        for i in range(len(vols)):
            vols[i] = self.get_volatility(strikes[i])
        ax1.plot(strikes, vols, label="Volatility Smile")
        plt.legend()
        plt.show()
        return fig


class Surface:
    def __init__(self, strikes: np.array, vols: np.array, times: np.array) -> None:
        self._strikes = strikes
        self._vols = vols
        self._times = times

    @property
    def strikes(self) -> np.array:
        return self._strikes

    @property
    def times(self):
        return self._times

    @property
    def vols(self) -> np.array:
        return self._vols


class SurfaceView(Surface):
    def __init__(self, strikes: np.array, implied_vols: np.array, times: np.array) -> None:
        super(SurfaceView, self).__init__(strikes, implied_vols, times)

    def get_volatility(self, time, strike):
        values = np.meshgrid(self.times, self.strikes)
        pairs = []
        for i in range(len(values[0][1])):
            for j in range(len(values[1])):
                pairs.append([values[0][1][i], values[1][j][0]])
        z = np.array(self.vols)
        z = z.swapaxes(0, 1).flatten()
        grid_z2 = griddata(pairs, z, (time, strike), method='cubic')
        return float(grid_z2)

    def plot_surface(self):
        times, strikes = np.meshgrid(self.times, self.strikes)
        fig = plt.figure(figsize=(9, 6))
        ax = fig.gca(projection='3d')
        ax.plot_surface(times, strikes, self.vols, rstride=2, cstride=2,
                        cmap=mpl.cm.coolwarm,
                        linewidth=0.5, antialiased=True)
        ax.set_xlabel('times')
        ax.set_ylabel('strikes')
        ax.set_zlabel('IV (%)')
        plt.show()

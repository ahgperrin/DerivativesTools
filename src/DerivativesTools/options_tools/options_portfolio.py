from DerivativesTools.options_tools.options import Options
from datetime import datetime
from DerivativesTools.bs_pricer.greeks import *
from DerivativesTools.futures_tools.futures import Futures, Spot
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn")


class OptionPortfolio:
    def __init__(self, spot: float, strategy_name: str = "") -> None:
        self.spot = spot
        self.name = strategy_name
        self.instrument: [Options, Futures, Spot] = []
        self.maturity_spots = np.arange(0, spot * 2, spot / 1000)
        self.payoffs = np.zeros_like(self.maturity_spots)
        self.premiums = 0
        self.delta = 0
        self.gamma = 0
        self.vega = 0
        self.theta = 0
        self.rho = 0

    def destroy(self):
        self.delta = 0
        self.gamma = 0
        self.vega = 0
        self.theta = 0
        self.rho = 0

    def update_greeks(self, spot: float, computation_date: datetime, base: int):
        self.spot = spot
        self.destroy()
        for ins in self.instrument:
            if isinstance(ins, Options):
                tt_maturity = (ins.maturity_datetime - computation_date).total_seconds() / (base * 86400)
                params = BsParams(ins.opt_type, ins.implied_vol, tt_maturity, ins.risk_free_rate,
                                  ins.dividend, spot, ins.strike)
                carac = option_carac(params, ins.side)
                self.delta += (carac.get("Delta") * ins.qty)
                self.gamma += (carac.get("Gamma") * ins.qty)
                self.theta += (carac.get("Theta") * ins.qty)
                self.vega += (carac.get("Vega") * ins.qty)
                self.rho += (carac.get("Rho") * ins.qty)
            if isinstance(ins, Futures):
                self.delta += (ins.qty * 1)
            if isinstance(ins, Spot):
                self.delta += (ins.qty * 1)
        self.portfolio_sensibilities()

    def long_call(self, price: float, strike: float, maturity_datetime: datetime,
                  implied_vol: float, risk_free_rate: float, dividend: float, qty: float):
        self.instrument.append(
            Options("c", price, strike, 1, maturity_datetime, implied_vol, risk_free_rate, dividend, qty))
        payoff = np.array([max(s - strike, 0) - price for s in self.maturity_spots]) * qty
        self.payoffs = self.payoffs + payoff
        self.premiums = self.premiums - (price * qty)

    def short_call(self, price: float, strike: float, maturity_datetime: datetime,
                   implied_vol: float, risk_free_rate: float, dividend: float, qty: float):
        self.instrument.append(
            Options("c", price, strike, -1, maturity_datetime, implied_vol, risk_free_rate, dividend, qty))
        payoff = np.array([max(s - strike, 0) * -1 + price for s in self.maturity_spots]) * qty
        self.payoffs = self.payoffs + payoff
        self.premiums = self.premiums + (price * qty)

    def long_put(self, price: float, strike: float, maturity_datetime: datetime,
                 implied_vol: float, risk_free_rate: float, dividend: float, qty: float):
        self.instrument.append(
            Options("p", price, strike, 1, maturity_datetime, implied_vol, risk_free_rate, dividend, qty))
        payoff = np.array([max(strike - s, 0) - price for s in self.maturity_spots]) * qty
        self.payoffs = self.payoffs + payoff
        self.premiums = self.premiums - (price * qty)

    def short_put(self, price: float, strike: float, maturity_datetime: datetime,
                  implied_vol: float, risk_free_rate: float, dividend: float, qty: float):
        self.instrument.append(
            Options("p", price, strike, -1, maturity_datetime, implied_vol, risk_free_rate, dividend, qty))
        payoff = np.array([max(strike - s, 0) * -1 + price for s in self.maturity_spots]) * qty
        self.payoffs = self.payoffs + payoff
        self.premiums = self.premiums + (price * qty)

    def long_future(self, name: str, maturity: datetime, price: float, qty: float, contract_size: float) -> None:
        self.instrument.append(Futures(name, maturity, price, qty, contract_size))
        payoff = (self.maturity_spots - price) * qty
        self.payoffs += payoff
        self.delta += qty * 1.0

    def short_future(self, name: str, maturity: datetime, price: float, qty: float, contract_size: float) -> None:
        self.instrument.append(Futures(name, maturity, price, -qty, contract_size))
        payoff = (price - self.maturity_spots) * qty
        self.payoffs += payoff
        self.delta += -qty * 1.0

    def long_spot(self, name: str, qty: float, price: float) -> None:
        self.instrument.append(Spot(name, price, qty))
        payoff = (self.maturity_spots - price) * qty
        self.payoffs += payoff
        self.delta += qty * 1.0

    def short_spot(self, name: str, qty: float, price: float) -> None:
        self.instrument.append(Spot(name, price, -qty))
        payoff = (price - self.maturity_spots) * qty
        self.payoffs += payoff
        self.delta += -qty * 1.0

    def portfolio_sensibilities(self) -> None:
        print('====== PORTFOLIO DESCRIPTION ======\n'
              'Delta: ', self.delta, '\n',
              'Gamma: ', self.gamma, '\n',
              'Vega: ', self.vega, '\n',
              'Theta: ', self.theta, '\n',
              'Rho: ', self.rho, '\n',
              )

    def breakeven(self):
        interval = (self.maturity_spots[1] - self.maturity_spots[0]) * 2
        breakeven = []
        results = []
        for i in range(len(self.payoffs)):
            if self.payoffs[i] >= 0:
                results.append(self.maturity_spots[i])
        breakeven.append(results[0])
        for i in range(1, len(results), 1):
            if results[i] - results[i - 1] > interval:
                breakeven.append(results[i - 1])
                breakeven.append(results[i])
        breakeven.append(results[len(results) - 1])
        return breakeven

    def plot_strategy(self, var_breakeven: tuple = None, es_breakeven: tuple = None, min_max: tuple = None):
        fig = plt.figure(figsize=(12.5, 8))
        fig.suptitle(self.name)
        fig.canvas.set_window_title(self.name)
        ax1 = fig.add_subplot(111)
        ax1.set_xlabel("Asset Price Maturity")
        ax1.set_ylabel('Profit in $')
        ax1.plot(self.maturity_spots, self.payoffs, label="PnL Structure")
        ax1.fill_between(self.maturity_spots, self.payoffs,
                         where=(self.payoffs > 0), facecolor='g', alpha=0.4, label="Positive Pnl")
        ax1.fill_between(self.maturity_spots, self.payoffs,
                         where=(self.payoffs < 0), facecolor='r', alpha=0.4, label="Negative Pnl")
        ax1.axvline(self.spot, c='green', label="Spot: " + str(self.spot))
        if var_breakeven is None:
            pass
        else:
            ax1.axvline(var_breakeven[0], c="y", label="Var Down: " + str(var_breakeven[0]))
            ax1.axvline(var_breakeven[1], c="y", label="Var Up: " + str(var_breakeven[1]))
        if es_breakeven is None:
            pass
        else:
            ax1.axvline(es_breakeven[0], c="orange", label="ES Down: " + str(es_breakeven[0]))
            ax1.axvline(es_breakeven[1], c="orange", label="ES Up: " + str(es_breakeven[1]))
        if min_max is None:
            pass
        else:
            ax1.axvline(min_max[0], c="r", label="Minimum: " + str(min_max[0]))
            ax1.axvline(min_max[1], c="r", label="Maximum: " + str(min_max[1]))

        plt.legend()
        plt.show()
        return fig

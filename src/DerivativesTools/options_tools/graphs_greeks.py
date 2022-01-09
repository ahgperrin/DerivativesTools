from DerivativesTools.options_tools.options_portfolio import *
from datetime import datetime

import matplotlib.pyplot as plt

plt.style.use('bmh')


def fig_plot(delta_list: list, vega_list: list, gamma_list: list, theta_list: list, rho_list: list, exog: str,
             exog_list: np.ndarray):
    fig = plt.figure(figsize=(7, 5), dpi=100)
    fig.suptitle("Evolution of Greeks for a variation of " + str(exog))
    ax1 = fig.add_subplot(511)
    ax1.plot(exog_list, delta_list, label='Delta')
    ax1.legend(loc=0)
    ax1.get_xaxis().set_visible(False)
    ax2 = fig.add_subplot(512)
    ax2.plot(exog_list, theta_list, label='Theta')
    ax2.legend(loc=0)
    ax2.get_xaxis().set_visible(False)
    ax3 = fig.add_subplot(513)
    ax3.plot(exog_list, rho_list, label='Rho')
    ax3.legend(loc=0)
    ax3.get_xaxis().set_visible(False)
    ax4 = fig.add_subplot(514)
    ax4.plot(exog_list, gamma_list, label='Gamma')
    ax4.legend(loc=0)
    ax4.get_xaxis().set_visible(False)
    ax5 = fig.add_subplot(515)
    ax5.plot(exog_list, vega_list, label='Vega')
    ax5.legend(loc=0)
    plt.legend()
    plt.show()
    return fig


def spot_sensi(portfolio: OptionPortfolio, spot, basis: int, computation_date: datetime, graphs: bool = False):
    delta_list = []
    gamma_list = []
    vega_list = []
    theta_list = []
    rho_list = []
    lin_spot = np.arange(0.5, spot * 2, spot / 1000)

    for spots in lin_spot:
        l_delta: float = 0
        l_gamma: float = 0
        l_vega: float = 0
        l_theta: float = 0
        l_rho: float = 0
        for ins in portfolio.instrument:
            if isinstance(ins, Options):
                yearly = basis * 24 * 60 * 60
                tt_maturity = (ins.maturity_datetime - computation_date).total_seconds() / yearly
                ins_copy = ins
                params = BsParams(ins_copy.opt_type, ins_copy.implied_vol, tt_maturity, ins_copy.risk_free_rate,
                                  ins_copy.dividend, spots, ins_copy.strike)
                carac = dict(option_carac(params, ins_copy.side))
                l_delta = l_delta + carac.get("Delta")
                l_gamma = l_gamma + carac.get("Gamma")
                l_vega = l_vega + carac.get("Vega")
                l_theta = l_theta + carac.get("Theta")
                l_rho = l_rho + carac.get("Rho")
            if isinstance(ins, Futures):
                l_delta = l_delta + (ins.qty * 1)
            if isinstance(ins, Spot):
                l_delta = l_delta + (ins.qty * 1)
        delta_list.append(l_delta)
        gamma_list.append(l_gamma)
        vega_list.append(l_vega)
        theta_list.append(l_theta)
        rho_list.append(l_rho)
    if graphs:
        fig_plot(delta_list, vega_list, gamma_list, theta_list, rho_list, "Spot", lin_spot)
    else:
        return delta_list, gamma_list, vega_list, theta_list, rho_list


def volatility_sensi(portfolio: OptionPortfolio, spot, basis: int, computation_date: datetime, graphs: bool = False):
    delta_list = []
    gamma_list = []
    vega_list = []
    theta_list = []
    rho_list = []
    lin_vol = np.arange(0.05, 2, 0.01)

    for vols in lin_vol:
        l_delta: float = 0
        l_gamma: float = 0
        l_vega: float = 0
        l_theta: float = 0
        l_rho: float = 0
        for ins in portfolio.instrument:
            if isinstance(ins, Options):
                yearly = basis * 24 * 60 * 60
                tt_maturity = (ins.maturity_datetime - computation_date).total_seconds() / yearly
                ins_copy = ins
                params = BsParams(ins_copy.opt_type, vols, tt_maturity, ins_copy.risk_free_rate,
                                  ins_copy.dividend, spot, ins_copy.strike)
                carac = dict(option_carac(params, ins_copy.side))
                l_delta = l_delta + carac.get("Delta")
                l_gamma = l_gamma + carac.get("Gamma")
                l_vega = l_vega + carac.get("Vega")
                l_theta = l_theta + carac.get("Theta")
                l_rho = l_rho + carac.get("Rho")
            if isinstance(ins, Futures):
                l_delta = l_delta + (ins.qty * 1)
            if isinstance(ins, Spot):
                l_delta = l_delta + (ins.qty * 1)
        delta_list.append(l_delta)
        gamma_list.append(l_gamma)
        vega_list.append(l_vega)
        theta_list.append(l_theta)
        rho_list.append(l_rho)
    if graphs:
        fig_plot(delta_list, vega_list, gamma_list, theta_list, rho_list, "Volatility", lin_vol)
    else:
        return delta_list, gamma_list, vega_list, theta_list, rho_list


def rate_sensi(portfolio: OptionPortfolio, spot, basis: int, computation_date: datetime, graphs: bool = False):
    delta_list = []
    gamma_list = []
    vega_list = []
    theta_list = []
    rho_list = []
    lin_rate = np.arange(-10, 20, 0.01)

    for rates in lin_rate:
        l_delta: float = 0
        l_gamma: float = 0
        l_vega: float = 0
        l_theta: float = 0
        l_rho: float = 0
        for ins in portfolio.instrument:
            if isinstance(ins, Options):
                yearly = basis * 24 * 60 * 60
                tt_maturity = (ins.maturity_datetime - computation_date).total_seconds() / yearly
                ins_copy = ins
                params = BsParams(ins_copy.opt_type, ins_copy.implied_vol, tt_maturity, rates,
                                  ins_copy.dividend, spot, ins_copy.strike)
                carac = dict(option_carac(params, ins_copy.side))
                l_delta = l_delta + carac.get("Delta")
                l_gamma = l_gamma + carac.get("Gamma")
                l_vega = l_vega + carac.get("Vega")
                l_theta = l_theta + carac.get("Theta")
                l_rho = l_rho + carac.get("Rho")
            if isinstance(ins, Futures):
                l_delta = l_delta + (ins.qty * 1)
            if isinstance(ins, Spot):
                l_delta = l_delta + (ins.qty * 1)
        delta_list.append(l_delta)
        gamma_list.append(l_gamma)
        vega_list.append(l_vega)
        theta_list.append(l_theta)
        rho_list.append(l_rho)
    if graphs:
        fig_plot(delta_list, vega_list, gamma_list, theta_list, rho_list, "Rates", lin_rate)
    else:
        return delta_list, gamma_list, vega_list, theta_list, rho_list


def time_sensi(portfolio: OptionPortfolio, spot, basis: int, graphs: bool = False):
    delta_list = []
    gamma_list = []
    vega_list = []
    theta_list = []
    rho_list = []
    lin_time = -np.sort(-np.arange(0, 365, 1))

    for times in lin_time:
        l_delta: float = 0
        l_gamma: float = 0
        l_vega: float = 0
        l_theta: float = 0
        l_rho: float = 0
        for ins in portfolio.instrument:
            if isinstance(ins, Options):
                yearly = basis * 24 * 60 * 60
                tt_maturity = times * 24 * 60 * 60
                tt_maturity = tt_maturity / yearly
                ins_copy = ins
                params = BsParams(ins_copy.opt_type, ins_copy.implied_vol, tt_maturity, ins_copy.risk_free_rate,
                                  ins_copy.dividend, spot, ins_copy.strike)
                carac = dict(option_carac(params, ins_copy.side))
                l_delta = l_delta + carac.get("Delta")
                l_gamma = l_gamma + carac.get("Gamma")
                l_vega = l_vega + carac.get("Vega")
                l_theta = l_theta + carac.get("Theta")
                l_rho = l_rho + carac.get("Rho")
            if isinstance(ins, Futures):
                l_delta = l_delta + (ins.qty * 1)
            if isinstance(ins, Spot):
                l_delta = l_delta + (ins.qty * 1)
        delta_list.append(l_delta)
        gamma_list.append(l_gamma)
        vega_list.append(l_vega)
        theta_list.append(l_theta)
        rho_list.append(l_rho)
    if graphs:
        fig_plot(delta_list, vega_list, gamma_list, theta_list, rho_list, "Time", lin_time)
    else:
        return delta_list, gamma_list, vega_list, theta_list, rho_list

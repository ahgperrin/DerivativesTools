def fx_forward(spot: float, rate_term: float, rate_base: float, base_term: int, base_base: int,
               tt_maturity: float) -> float:
    return (spot * (
                ((1 + rate_term * (tt_maturity / base_term)) / (1 + rate_base * (tt_maturity / base_base))) - 1)) + spot


def swap_points(spot: float, rate_term: float, rate_base: float, base_term: int, base_base: int,
                tt_maturity: float) -> float:
    return fx_forward(spot, rate_term, rate_base, base_term, base_base, tt_maturity) - spot


def implied_rate_cc1(spot: float, swap: float, rate_cc2: float, base_cc2: int, base_cc1: int,
                     tt_maturity: float) -> float:
    return ((((1 + (rate_cc2 * (tt_maturity / base_cc2))) * spot) / (spot + swap)) - 1) * (base_cc1 / tt_maturity)


def implied_rate_cc2(spot: float, swap: float, rate_cc1: float, base_cc2: int, base_cc1: int,
                     tt_maturity: float) -> float:
    return ((((1 + (rate_cc1 * (tt_maturity / base_cc1))) * (spot + swap)) / spot) - 1) * (base_cc2 / tt_maturity)

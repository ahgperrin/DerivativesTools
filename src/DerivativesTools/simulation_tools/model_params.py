class GeometricBrownianParams:

    def __init__(self, mu: float, sigma: float, tt_maturity: float, delta: int, spot_zero: float) -> None:
        self._mu = mu
        self._sigma = sigma
        self._tt_maturity = tt_maturity
        self._delta = delta
        self._spot_zero = spot_zero

    @property
    def mu(self) -> float:
        return self._mu

    @mu.setter
    def mu(self, value: float) -> None:
        self._mu = value

    @property
    def sigma(self) -> float:
        return self._sigma

    @sigma.setter
    def sigma(self, value: float) -> None:
        self._sigma = value

    @property
    def tt_maturity(self) -> float:
        return self._tt_maturity

    @tt_maturity.setter
    def tt_maturity(self, value: float) -> None:
        self._tt_maturity = value

    @property
    def delta(self) -> int:
        return self._delta

    @delta.setter
    def delta(self, value: int) -> None:
        self._delta = value

    @property
    def spot_zero(self) -> float:
        return self._spot_zero

    @spot_zero.setter
    def spot_zero(self, value: float) -> None:
        self._spot_zero = value

    @property
    def params(self) -> dict:
        return {
            "mu": self._mu,
            "sigma": self._sigma,
            "tt_maturity": self._tt_maturity,
            "delta": self._delta,
            "spot_zero": self._spot_zero
        }

    def print_model(self) -> None:
        print("=== Geometric Brownian Motion ===")
        print("=================================")
        print("Process Mean : ", self.params.get("mu"))
        print("Process Volatility : ", self.params.get("sigma"))
        print("Process Time to maturity : ", self.params.get("tt_maturity"))
        print("Process Delta Time : ", self.params.get("delta"))
        print("Process Spot : ", self.params.get("spot_zero"))
        print("=================================")


class JumpDiffusionParams:

    def __init__(self, mu: float, sigma: float, tt_maturity: float, delta: int, spot_zero: float, jumps_lambda: float,
                 jumps_mu: float, jumps_sigma: float) -> None:
        self._mu = mu
        self._sigma = sigma
        self._tt_maturity = tt_maturity
        self._delta = delta
        self._spot_zero = spot_zero
        self._j_lambda = jumps_lambda
        self._j_mu = jumps_mu
        self._j_sigma = jumps_sigma

    @property
    def mu(self) -> float:
        return self._mu

    @mu.setter
    def mu(self, value: float) -> None:
        self._mu = value

    @property
    def sigma(self) -> float:
        return self._sigma

    @sigma.setter
    def sigma(self, value: float) -> None:
        self._sigma = value

    @property
    def tt_maturity(self) -> float:
        return self._tt_maturity

    @tt_maturity.setter
    def tt_maturity(self, value: float) -> None:
        self._tt_maturity = value

    @property
    def delta(self) -> int:
        return self._delta

    @delta.setter
    def delta(self, value: int) -> None:
        self._delta = value

    @property
    def spot_zero(self) -> float:
        return self._spot_zero

    @spot_zero.setter
    def spot_zero(self, value: float) -> None:
        self._spot_zero = value

    @property
    def j_lambda(self) -> float:
        return self._j_lambda

    @j_lambda.setter
    def j_lambda(self, value: float) -> None:
        self._j_lambda = value

    @property
    def j_mu(self) -> float:
        return self._j_mu

    @j_mu.setter
    def j_mu(self, value: float) -> None:
        self._j_mu = value

    @property
    def j_sigma(self) -> float:
        return self._j_sigma

    @j_sigma.setter
    def j_sigma(self, value: float) -> None:
        self._j_sigma = value

    @property
    def params(self) -> dict:
        return {
            "mu": self._mu,
            "sigma": self._sigma,
            "jump_lambda": self._j_lambda,
            "jump_mean": self._j_mu,
            "jump_sigma": self._j_sigma,
            "tt_maturity": self._tt_maturity,
            "delta": self._delta,
            "spot_zero": self._spot_zero
        }

    def print_model(self):
        print("===== Merton Jump Diffusion =====")
        print("=================================")
        print("Diffusion Mean : ", self.params.get("mu"))
        print("Diffusion Volatility : ", self.params.get("sigma"))
        print("Jumps Mean : ", self.params.get("jump_mean"))
        print("Jumps Volatility : ", self.params.get("jump_sigma"))
        print("Jumps Lambda : ", self.params.get("jump_lambda"))
        print("Process Time to maturity : ", self.params.get("tt_maturity"))
        print("Process Delta Time : ", self.params.get("delta"))
        print("Process Spot : ", self.params.get("spot_zero"))
        print("=================================")


class HestonParams:

    def __init__(self, mu: float, tt_maturity: float, delta: int, spot_zero: float, vol_zero: float, alpha: float,
                 sigma_vol: float, mu_vol: float, covariance: float) -> None:
        self._mu = mu
        self._tt_maturity = tt_maturity
        self._delta = delta
        self._spot_zero = spot_zero
        self._alpha = alpha
        self._sigma_vol = sigma_vol
        self._mu_vol = mu_vol
        self._covariance = covariance
        self._vol_zero = vol_zero

    @property
    def mu(self) -> float:
        return self._mu

    @mu.setter
    def mu(self, value: float) -> None:
        self._mu = value

    @property
    def tt_maturity(self) -> float:
        return self._tt_maturity

    @tt_maturity.setter
    def tt_maturity(self, value: float) -> None:
        self._tt_maturity = value

    @property
    def delta(self) -> int:
        return self._delta

    @delta.setter
    def delta(self, value: int) -> None:
        self._delta = value

    @property
    def spot_zero(self) -> float:
        return self._spot_zero

    @spot_zero.setter
    def spot_zero(self, value: float) -> None:
        self._spot_zero = value

    @property
    def vol_zero(self) -> float:
        return self._vol_zero

    @vol_zero.setter
    def vol_zero(self, value: float) -> None:
        self._vol_zero = value

    @property
    def alpha(self) -> float:
        return self._alpha

    @alpha.setter
    def alpha(self, value: float) -> None:
        self._alpha = value

    @property
    def sigma_vol(self) -> float:
        return self._sigma_vol

    @sigma_vol.setter
    def sigma_vol(self, value: float) -> None:
        self._sigma_vol = value

    @property
    def mu_vol(self) -> float:
        return self._mu_vol

    @mu_vol.setter
    def mu_vol(self, value: float) -> None:
        self._mu_vol = value

    @property
    def covariance(self) -> float:
        return self._covariance

    @covariance.setter
    def covariance(self, value: float) -> None:
        self._covariance = value

    @property
    def params(self) -> dict:
        return {
            "mu": self._mu,
            "alpha": self._alpha,
            "sigma_vol": self._sigma_vol,
            "mu_vol": self._mu_vol,
            "covariance": self._covariance,
            "vol_zero": self._vol_zero,
            "tt_maturity": self._tt_maturity,
            "delta": self._delta,
            "spot_zero": self._spot_zero
        }

    def print_model(self):
        print("=== Heston Stochastic Volatility Process ===")
        print("============================================")
        print("Diffusion Mean : ", self.params.get("mu"))
        print("Starting volatility :", self.params.get("vol_zero"))
        print("Volatility Mean Reversion Speed : ", self.params.get("alpha"))
        print("Vol of Volatility : ", self.params.get("sigma_vol"))
        print("Long term Volatility Mean : ", self.params.get("mu_vol"))
        print("Covariance Between spot and vol : ", self.params.get("covariance"))
        print("Process Time to maturity : ", self.params.get("tt_maturity"))
        print("Process Delta Time : ", self.params.get("delta"))
        print("Process Spot : ", self.params.get("spot_zero"))
        print("============================================")


class OrnsteinUhlenbeckParams:

    def __init__(self, theta: float, sigma: float, tt_maturity: float, delta: int, spot_zero: float,
                 kappa: float) -> None:
        self._theta = theta
        self._sigma = sigma
        self._kappa = kappa
        self._tt_maturity = tt_maturity
        self._delta = delta
        self._spot_zero = spot_zero

    @property
    def theta(self) -> float:
        return self._theta

    @theta.setter
    def theta(self, value: float) -> None:
        self._theta = value

    @property
    def tt_maturity(self) -> float:
        return self._tt_maturity

    @tt_maturity.setter
    def tt_maturity(self, value: float) -> None:
        self._tt_maturity = value

    @property
    def delta(self) -> int:
        return self._delta

    @delta.setter
    def delta(self, value: int) -> None:
        self._delta = value

    @property
    def spot_zero(self) -> float:
        return self._spot_zero

    @spot_zero.setter
    def spot_zero(self, value: float) -> None:
        self._spot_zero = value

    @property
    def kappa(self) -> float:
        return self._kappa

    @kappa.setter
    def kappa(self, value: float) -> None:
        self._kappa = value

    @property
    def sigma(self) -> float:
        return self._sigma

    @sigma.setter
    def sigma(self, value: float) -> None:
        self._sigma = value

    @property
    def params(self) -> dict:
        return {
            "theta": self._theta,
            "kappa": self._kappa,
            "sigma": self._sigma,
            "tt_maturity": self._tt_maturity,
            "delta": self._delta,
            "spot_zero": self._spot_zero
        }

    def print_model(self):
        print("======== Ornstein-Uhlenbeck Process ========")
        print("============================================")
        print("Diffusion Mean : ", self.params.get("theta"))
        print("Process Mean Reversion Speed : ", self.params.get("kappa"))
        print("Volatility : ", self.params.get("sigma"))
        print("Process Time to maturity : ", self.params.get("tt_maturity"))
        print("Process Delta Time : ", self.params.get("delta"))
        print("Process Spot : ", self.params.get("spot_zero"))
        print("============================================")


class ConstantElasticityParams:

    def __init__(self, mu: float, sigma: float, tt_maturity: float, delta: int, spot_zero: float,
                 gamma: float) -> None:
        self._mu = mu
        self._sigma = sigma
        self._gamma = gamma
        self._tt_maturity = tt_maturity
        self._delta = delta
        self._spot_zero = spot_zero

    @property
    def mu(self) -> float:
        return self._mu

    @mu.setter
    def mu(self, value: float) -> None:
        self._mu = value

    @property
    def tt_maturity(self) -> float:
        return self._tt_maturity

    @tt_maturity.setter
    def tt_maturity(self, value: float) -> None:
        self._tt_maturity = value

    @property
    def delta(self) -> int:
        return self._delta

    @delta.setter
    def delta(self, value: int) -> None:
        self._delta = value

    @property
    def spot_zero(self) -> float:
        return self._spot_zero

    @spot_zero.setter
    def spot_zero(self, value: float) -> None:
        self._spot_zero = value

    @property
    def gamma(self) -> float:
        return self._gamma

    @gamma.setter
    def gamma(self, value: float) -> None:
        self._gamma = value

    @property
    def sigma(self) -> float:
        return self._sigma

    @sigma.setter
    def sigma(self, value: float) -> None:
        self._sigma = value

    @property
    def params(self) -> dict:
        return {
            "mu": self._mu,
            "gamma": self._gamma,
            "sigma": self._sigma,
            "tt_maturity": self._tt_maturity,
            "delta": self._delta,
            "spot_zero": self._spot_zero
        }

    def print_model(self):
        print("======== Ornstein-Uhlenbeck Process ========")
        print("============================================")
        print("Diffusion Mean : ", self.params.get("mu"))
        print("Process Elasticity : ", self.params.get("gamma"))
        print("Volatility : ", self.params.get("sigma"))
        print("Process Time to maturity : ", self.params.get("tt_maturity"))
        print("Process Delta Time : ", self.params.get("delta"))
        print("Process Spot : ", self.params.get("spot_zero"))
        print("============================================")

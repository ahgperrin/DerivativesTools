
-----------------
# DerivativesTools - Python Powerful Derivatives Management

-----------------
# DESCRIPTION

*DerivativesTools* is 100% python packages that contains different function regarding derivatives pricing, derivatives
portfolio management, simulation and graphical representation (payoff, greeks, volatility...)

-----------------
# TABLE OF CONTENT

-----------------
1. [Installation](#Installation)
2. [Structure and import framework](#Structure-and-import-framework)
   1. [ Structure](#Structure)
   2. [Import Framework](#Import-Framework)
3. [Sub Packages](#Sub-Packages)
   1. [bs_pricer](#bs_pricer)
   2. [futures_tools](#futures_tools)
   3. [fx_pricer](#fx_pricer)
   4. [options_tools](#options_tools)
   5. [simulation_tools](#simulation_tools)
4. [Future Release](#Future-Release)

# Installation
In order to install this package into your machine, you will need of course
a python interpreter, git and pip, installed on your machine.
Open a terminal (macOS) or a cmd (windows)
Then choose the folder where you want to copy source code :
```sh
cd yourFolder
```
Then you clone the git repository
```sh
git clone https://github.com/ahgperrin/DerivativesTools.git
```
Then select the project and install it :
```sh
cd DerivativeTools
pip install --user .
```

# Structure and import framework
When the package is installed on your machine you will need to learn 
about features, structure and import framework.
The project is build like that :<br>
## Structure
PACKAGE CONTENTS<br>
&emsp; &emsp; bs_pricer (package)<br>
&emsp; &emsp; &emsp; &emsp; bs_params (Module)<br>
&emsp; &emsp; &emsp; &emsp; greeks (Module)<br>
&emsp; &emsp; &emsp; &emsp; implied_solver (Module)<br>
&emsp; &emsp; &emsp; &emsp; pricing (Module)<br>

&emsp; &emsp; futures_tools (package)<br>
&emsp; &emsp; &emsp; &emsp; futures (Module)<br>

&emsp; &emsp; fx_pricer (package)<br>
&emsp; &emsp; &emsp; &emsp; fx_pricer (Module)<br>

&emsp; &emsp; options_tools (package)<br>
&emsp; &emsp; &emsp; &emsp; graphs_greeks (Module)<br>
&emsp; &emsp; &emsp; &emsp; options (Module)<br>
&emsp; &emsp; &emsp; &emsp; options_portfolio (Module)<br>
&emsp; &emsp; &emsp; &emsp; vol_structure (Module)<br>

&emsp; &emsp; simulation_tools (package)<br>
&emsp; &emsp; &emsp; &emsp; correlated_portfolio (Module)<br>
&emsp; &emsp; &emsp; &emsp; geometric_brownian (Module)<br>
&emsp; &emsp; &emsp; &emsp; heston (Module)<br>
&emsp; &emsp; &emsp; &emsp; merton_jump_diff (Module)<br>
&emsp; &emsp; &emsp; &emsp; model_params (Module)<br>
&emsp; &emsp; &emsp; &emsp; ornstein_uhlenbeck (Module)<br>
&emsp; &emsp; &emsp; &emsp; simulation_computation (Module)<br>
&emsp; &emsp; &emsp; &emsp; tools (Module)<br>

## Import Framework
```pycon
# Import a module to use it as reference
import DerivativesTools.bs_pricer.pricing as p
import DerivativesTools.fx_pricer.fx_pricer as fx
import DerivativesTools.futures_tools.futures as f
import DerivativesTools.options_tools.options_portfolio as port 
import DerivativesTools.simulation_tools.merton_jump_diff as jump_diff 
```

# Sub Packages
## bs_pricer
*bs_pricer* is a package that contains all function in order to price
european options using black and scholes model.
The package contains four modules: bs_params (parameters class), greeks (greeks computation)
implied_solver (solving volatility from prices), pricing (pricing function).
### pricing
```pycon
import DerivativesTools.bs_pricer.pricing as p
# Calculate time in years
delta_t = p.time_maturity(datetime.now(),datetime(2022,2,18,9),365)
# Define parameters (example SPY C4700 Feb 18 22)
spy_c_4700 = p.BsParams("c",0.1525,delta_t,-0.0049,0.02,4668.13,4700)
# get price
p.option_price(spy_c_4700)
Out[10]: 67.03249036777743
# get_moneyness
p.moneyness(spy_c_4700)
Out[11]: 0.9932191489361702
# get prod D1 prob D2, drift
Out[13]: -0.17303863402181574
p.d2(spy_c_4700)
Out[14]: -0.219468651125529
p.drift(spy_c_4700)
Out[15]: -0.0012302412436982584
```
### greeks
```pycon
import DerivativesTools.bs_pricer.greeks as g
# With the same example as for pricing
g.option_carac(spy_c_4700,side=1)
Out[18]: 
{'Price': 67.03249036777743,
 'Volatility': 0.1525,
 'Delta': 0.4305116610820689,
 'Vega': 8.893462573618294,
 'Rho': -2.5579130508717824,
 'Theta': -1.120305076879068,
 'Omega': 29.98075096749046,
 'Gamma': 0.0018099277375870364,
 'Vanna': 0.005645542382588186,
 'Vomma': 0.02214708694529415}
# Can be computed individually 
g.vega(spy_c_4700,side=-1)
Out[19]: -8.893462573618294
g.theta(spy_c_4700,side=-1)
Out[20]: 1.120305076879068
```
### implied_solver
```pycon
import DerivativesTools.bs_pricer.implied_solver as solve
# Solve the volatility of our example option if the price is 80$
solve.implied_vol(spy_c_4700,80)
Out[22]: 0.17570040502571693
# Solve smile of call for this maturity given price et strike
strikes = [3500,3700,3900,4100,4300,4500,4700]
prices = [1170.15,971.24,773.53,578.63,389.90,214.97,73.08]
solve.volatility_smile(strikes,prices,spy_c_4700)
Out[25]: 
array([0.55088305, 0.46937067, 0.3947695 , 0.3285587 , 0.27001135,
       0.21610441, 0.16333316])
# Solve surface given price, strikes, and times
strikes = [3500,3700,3900,4100,4300,4500,4700]
times = [delta_t,p.time_maturity(datetime.now(),datetime(2022,3,18,9),365),p.time_maturity(datetime.now(),datetime(2022,6,17,9),365)]
prices = [[1170.15,1171.73,1193.21],[971.24,975.70,990.24],[773.53,782.27,824.66],
          [578.63,593.40,649.53],[389.90,412.92,482.53],[214.97,245.56,329.19],
          [73.08,105.90,195.30]]
solve.volatility_surface(strikes,times,prices,spy_c_4700)
Out[70]: 
array([[0.45039449, 0.36510866, 0.32090798],
       [0.39074959, 0.33293169, 0.2654696 ],
       [0.33751239, 0.30039171, 0.27685892],
       [0.29056983, 0.2676429 , 0.25393176],
       [0.24691772, 0.2348904 , 0.22909017],
       [0.20304341, 0.19822715, 0.20403733],
       [0.15650284, 0.15987016, 0.17808935]])
```
## futures_tools
## fx_pricer
## options_tools
### vol_structure
Given the same datas as for example in bs_pricer implied_solver. 
With this module you can interpolate, and plot smile and surface.
```pycon
import DerivativesTools.options_tools.vol_structure as vol
smile_spy_FEB22 = vol.SmileView(strikes = [3500,3700,3900,4100,4300,4500,4700],
                                implied_vols = [0.55088305, 0.46937067, 0.3947695 , 0.3285587 , 0.27001135,
                                    0.21610441, 0.16333316])
smile_spy_FEB22.get_volatility(strike=3550)
Out[79]: 0.5299617374218752
smile_spy_FEB22.plot_smile()
```
![](https://github.com/ahgperrin/DerivativesTools/blob/master/examples/smile.png?raw=true)
## simulation_tools
# Future Release

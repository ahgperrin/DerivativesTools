
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
```sh
# Import a module to use it as reference
import DerivativesTools.bs_pricer.pricing as p
import DerivativesTools.fx_pricer.fx_pricer as fx
import DerivativesTools.futures_tools.futures as f
import DerivativesTools.options_tools.options_portfolio as port 
import DerivativesTools.simulation_tools.merton_jump_diff as jump_diff 
```

# Sub Packages
## bs_pricer

## futures_tools
## fx_pricer
## options_tools
## simulation_tools
# Future Release
from setuptools import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='DerivativesTools',
    version='0.0.2',
    author=["Antoine Perrin", "Florent Segondi"],
    author_email=["antoineperrin.pro1@gmail.com", "florent.segondi@gmail.com"],
    py_modules=["bs_params"
                "greeks",
                "implied_solver",
                "pricing",
                "futures",
                "fx_pricer",
                "graphs_greeks",
                "options",
                "options_portfolio",
                "vol_structure",
                "correlated_portfolio",
                "geometric_brownian",
                "heston",
                "merton_jump_diffusion",
                "model_params",
                "ornstein_uhlenbeck",
                "simulation_computation",
                "tools"],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    description='Python Library for Derivatives Management, Pricing & simulation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["matplotlib", "pandas", "numpy",
                      "scipy", "typing", "sklearn",
                      "arch", "seaborn", "statsmodels"],
)

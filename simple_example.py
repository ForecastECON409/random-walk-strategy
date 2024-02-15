# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: py:percent,ipynb
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
# ---

# %% [markdown]
# # Random Walk Simple Example
#
# Here's a simple example where we produce a set of plots, called a tear sheet, for a single stock.
# %% [markdown]
"""
Small demonstration of the `pyfolio` library. We will use the `GBPUSD` exchange rate to show the basic functionality of the library.
"""
# %%
# silence warnings raised by the pyfolio library.
import warnings
warnings.filterwarnings('ignore')

# %%
import yfinance as yf
import pyfolio as pf
import pandas as pd
import os
import numpy as np
# %%
s = yf.download(
    tickers='GBPUSD=X',
    start='2003-11-01'
)
# %%
# Drop timezone information to avoid errors with pyfolio.
s.index = s.index.tz_localize('utc')
# %%
# Calculating the returns as the percentage change of the close
# exchange rate.
s_returns = s.Close.pct_change()
# %% [markdown]
r"""
The signal of the strategy is calculated as follows:

$$
signal_t = \begin{cases}
    1 &  \%\Delta \hat{s}_{t} > 0 \\
    -1 &  \%\Delta \hat{s}_{t} < 0 \\
\end{cases}
$$

Where $\%\Delta \hat{s}_{t}$ is forecasted percentage change of the exchange rate at time $t$ given the information available at time $t-1$.
"""
# %% [markdown]
r"""
The random walk model is defined as:

$$
\% \Delta s_{t} = \% \Delta s_{t-1} + \epsilon_{t}
$$

where 

$$
\%\Delta \hat{s}_{t} = \% \Delta s_{t-1}
$$
"""
# %% [markdown]
r"""
The returns of the random walk strategy are calculated as follows:

$$
r^{rw}_{t} = signal_{t} \times \%\Delta s_{t}
$$
"""
# %%
rw_returns = (
    s_returns.shift(1)
    .pipe(np.sign)
    .pipe(lambda x: x * s_returns)
    .dropna()
)
# %%
# Tear sheet for the random walk strategy. No live trading is defined.
pf.create_returns_tear_sheet(rw_returns)

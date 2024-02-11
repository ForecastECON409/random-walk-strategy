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
# # Intro
#
# Here's a simple example where we produce a set of plots, called a tear sheet, for a single stock.

# %% [markdown]
# ## Imports and Settings

# %%
# silence warnings
import warnings
warnings.filterwarnings('ignore')

# %%
import yfinance as yf
import pyfolio as pf
import pandas as pd
import os
import numpy as np
# %%
data_path = os.path.join('data', 'GBPUSD.csv')
# %%
#s = yf.download(
    #tickers='GBPUSD=X',
    #start='2003-11-01'
#)
#s.to_csv(
    #os.path.join(
        #'data',
        #'GBPUSD.csv'
    #),
    #index=True
#)
s = pd.read_csv(data_path, index_col=0, parse_dates=True)
s.index = s.index.tz_localize('utc')
# %%
s_returns = s.Close.pct_change()
# %%
rw_returns = (
    s_returns.shift(1)
    .pipe(np.sign)
    .pipe(lambda x: x * s_returns)
    .dropna()
)
# %%
pf.create_returns_tear_sheet(rw_returns)

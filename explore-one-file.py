# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Explore SMLM data from tables
# ----------------------------------
#

# # IMPORTANT
# # Disable autosave for Jupytext version control with a paired .py script
# ## But manually saving the notebook frequently is still good

# %autosave 0

# ## Imports

# +
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# -

# ## Data path

rawdata_path = Path('C:/AutofluorescenceExp_CODI-0092_2025-09-19/blank_alc-ammonia/Blank_CRC_Ct3-2_Alc_Ammonia_fov1.csv')

# ## Load data from .csv

# ### ONI (CODI API download) version

datatable = pd.read_csv(
    rawdata_path, skiprows=1, names=[
        'x-nm', 'y-nm', 'frame', 'channel', 'duration-frames', 'var-x-nm2', 'var-y-nm2', 'var-intensity-photons', 'var-background-photons',
        'var-sigma-x-nm2', 'var-sigma-y-nm2', 'z-nm', 'bg-mean-photons', 'sigma-x-mean-nm', 'sigma-y-mean-nm', 'intensity-mean-photons',
        'presplit-channels-channel-index', 'channel-group-index', 'parent-id', 'cluster-id', 'outlier-score', 'bleeding-distance-nm'
    ]
)

datatable

# ### ONI - Add localisation precision and average PSF sigma

datatable['locprec-nm'] = (np.sqrt(datatable['var-x-nm2']) + np.sqrt(datatable['var-y-nm2'])) / 2
datatable['psf-sigma-nm'] = (datatable['sigma-x-mean-nm'] + datatable['sigma-y-mean-nm']) / 2

# ### Localisation parameter histograms

plt.hist(datatable['psf-sigma-nm'], bins=30, color='xkcd:sea green')
plt.show

plt.hist(datatable['locprec-nm'], bins=30, color='xkcd:sea green')
plt.show()

upper_photons_display = 30000
plt.hist(datatable['intensity-mean-photons'], bins=30, color='xkcd:sea green', range=[0, upper_photons_display])
plt.show()



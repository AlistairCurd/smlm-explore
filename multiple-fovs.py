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

# # Explore localisation data from multiple FOVs
# -------------------------------------------------

# ## IMPORTANT
# ## Disable autosave for Jupytext version control with a paired .py script
# ### But manually saving the notebook frequently is still good

# %autosave 0

# ## Imports

# +
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# -
# # Explore a single data directory
# Give the path here


rawdata_dirpath = Path('C:/Nephrin_CODI-0079_2025-10-13/30nm_locs-p0-05/')

# ## Load data
#
# ### Load tables from .csvs - downloaded using ONI API

# +
datatables = []
fovnames = []

for path_i in rawdata_dirpath.iterdir():
    datatable = pd.read_csv(
        path_i, skiprows=1, names=[
            'x-nm', 'y-nm', 'frame', 'channel', 'duration-frames', 'var-x-nm2', 'var-y-nm2', 'var-intensity-photons', 'var-background-photons',
            'var-sigma-x-nm2', 'var-sigma-y-nm2', 'z-nm', 'bg-mean-photons', 'sigma-x-mean-nm', 'sigma-y-mean-nm', 'intensity-mean-photons',
            'presplit-channels-channel-index', 'channel-group-index', 'parent-id', 'cluster-id', 'outlier-score', 'bleeding-distance-nm'
        ]
    )
    datatables.append(datatable)
    fovnames.append(path_i.stem)
# -

# ### Check things are as expected

# #### Number of datasets in directory

len(datatables)

# #### Display a dataset

datatables[0]

# #### List the names of the datasets

fovnames

# ### Add localisation precision and average PSF sigma

for datatable in datatables:
    datatable['locprec-nm'] = (np.sqrt(datatable['var-x-nm2']) + np.sqrt(datatable['var-y-nm2'])) / 2
    datatable['psf-sigma-nm'] = (datatable['sigma-x-mean-nm'] + datatable['sigma-y-mean-nm']) / 2

# ### Check again

datatables[0]

# ### Check localisation precision distribution for one fov

plt.hist(datatables[0]['locprec-nm'], bins=30, color='xkcd:sea green')
plt.show

# ## These are the available parameters to explore:

datatables[0].columns.to_list()

# ## Numbers of locs in the fovs

# +
nlocs = []

for datatable in datatables:
    nlocs.append(len(datatable))
# -

nlocs



# # You can compare data from FOVs from different directories, or from within one
# ## If desired, Use data separated out into relevant directoriesu
# ## List the directories here, by their full address (giving just one directory is ok too)
#
# List within square brackets, separated by commas

# +
# e.g.
# [
#
# 'C:/AutofluorescenceExp_CODI-0092_2025-09-19/blank_alc-ammonia/',
# 'C:/AutofluorescenceExp_CODI-0092_2025-09-19/blank_ammonium-chloride/',
# 'C:/AutofluorescenceExp_CODI-0092_2025-09-19/blank_ammonium-chl-w-NaBH4/',
#
# ]

datadir_paths_list = [

'C:/AutofluorescenceExp_CODI-0092_2025-09-19/blank_alc-ammonia/',
'C:/AutofluorescenceExp_CODI-0092_2025-09-19/blank_ammonium-chloride/',
'C:/AutofluorescenceExp_CODI-0092_2025-09-19/blank_ammonium-chl-w-NaBH4/',
'C:/AutofluorescenceExp_CODI-0092_2025-09-19/blank_commercial-quencher/',
'C:/AutofluorescenceExp_CODI-0092_2025-09-19/blank_invitrogen-quench-kit/',
'C:/AutofluorescenceExp_CODI-0092_2025-09-19/blank_NaBH4/',
'C:/AutofluorescenceExp_CODI-0092_2025-09-19/blank_no-quencher/',
    
]
# -

# ## Set up dataframe to compare summary statistics from FOVs, including from different directories

fovs_summary_df = pd.DataFrame(columns=['condition', 'fov_name', 'num_locs'])

# ## Populate

# +
for datadir_path in datadir_paths_list:
    rawdata_dirpath = Path(datadir_path)

    datatables = []
    fovnames = []
    
    for path_i in rawdata_dirpath.iterdir():
        datatable = pd.read_csv(
            path_i, skiprows=1, names=[
                'x-nm', 'y-nm', 'frame', 'channel', 'duration-frames', 'var-x-nm2', 'var-y-nm2', 'var-intensity-photons', 'var-background-photons',
                'var-sigma-x-nm2', 'var-sigma-y-nm2', 'z-nm', 'bg-mean-photons', 'sigma-x-mean-nm', 'sigma-y-mean-nm', 'intensity-mean-photons',
                'presplit-channels-channel-index', 'channel-group-index', 'parent-id', 'cluster-id', 'outlier-score', 'bleeding-distance-nm'
            ]
        )
        datatables.append(datatable)
        fovnames.append(path_i.stem)

    for datatable in datatables:
        datatable['locprec-nm'] = (np.sqrt(datatable['var-x-nm2']) + np.sqrt(datatable['var-y-nm2'])) / 2
        datatable['psf-sigma-nm'] = (datatable['sigma-x-mean-nm'] + datatable['sigma-y-mean-nm']) / 2

    for i, datatable in enumerate(datatables):
        fovs_summary_df = pd.concat(
            [fovs_summary_df, pd.DataFrame({
                'condition': [rawdata_dirpath.stem],
                'fov_name': [fovnames[i]],
                'num_locs': [len(datatable)]
                })
            ]
        )

fovs_summary_df.set_index('fov_name')
# -

# ## Plot summary of numbers of localisations

pd.plotting.boxplot(fovs_summary_df, column='num_locs', by='condition')
plt.xticks(rotation=90)
plt.savefig('C:/Temp/numbers-of-locs-by-autofl-quenching-method.pdf', bbox_inches='tight')
plt.show()



plt.scatter(fovs_summary_df['condition'], fovs_summary_df['num_locs'], s=5)
plt.xticks(rotation=90)
plt.show()

plt.scatter(fovs_summary_df['condition'], fovs_summary_df['num_locs'], s=5)
plt.xticks(rotation=90)
plt.ylim([0, 20000])
plt.show()

# ## Plot localisation parameter distributions

# One row for each condition, localisation precision and PSF size

# +
fig, axes = plt.subplots(len(datadir_paths_list), 2, figsize=(8, 13), layout='constrained')

for row, rawdata_dirpath in enumerate(datadir_paths_list):
    rawdata_dirpath = Path(rawdata_dirpath)

    datatables = []
    fovnames = []
    
    for path_i in rawdata_dirpath.iterdir():
        datatable = pd.read_csv(
            path_i, skiprows=1, names=[
                'x-nm', 'y-nm', 'frame', 'channel', 'duration-frames', 'var-x-nm2', 'var-y-nm2', 'var-intensity-photons', 'var-background-photons',
                'var-sigma-x-nm2', 'var-sigma-y-nm2', 'z-nm', 'bg-mean-photons', 'sigma-x-mean-nm', 'sigma-y-mean-nm', 'intensity-mean-photons',
                'presplit-channels-channel-index', 'channel-group-index', 'parent-id', 'cluster-id', 'outlier-score', 'bleeding-distance-nm'
            ]
        )
        datatables.append(datatable)
        fovnames.append(path_i.stem)

    for datatable in datatables:
        datatable['locprec-nm'] = (np.sqrt(datatable['var-x-nm2']) + np.sqrt(datatable['var-y-nm2'])) / 2
        datatable['psf-sigma-nm'] = (datatable['sigma-x-mean-nm'] + datatable['sigma-y-mean-nm']) / 2

        locprec_hist_values, edges = np.histogram(datatable['locprec-nm'], bins=30)
        bin_centres = (edges[0:-1] + edges[1:]) / 2
        axes[row, 0].plot(bin_centres, locprec_hist_values)

        psf_hist_values, edges = np.histogram(datatable['psf-sigma-nm'], bins=30)
        bin_centres = (edges[0:-1] + edges[1:]) / 2
        axes[row, 1].plot(bin_centres, psf_hist_values)

        axes[row, 0].set_ylabel(rawdata_dirpath.stem[6:], rotation=90)

axes[len(datadir_paths_list) - 1, 0].set_xlabel('loc-prec (nm)')
axes[len(datadir_paths_list) - 1, 1].set_xlabel('PSF sigma (nm)')

# -

fig.savefig('C:/Temp/locprec-and-psf-various-autofl-conditions.pdf', bbox_inches='tight')

# # Filter data

# ### Test/check on one FOV

datatables[0].columns

# +
#Test

datatable_in = datatables[0]
datatable_out = datatable_in[datatable_in['locprec-nm'] < 15]
datatable_out = datatable_out[datatable_out['outlier-score'] < 0.001]
# -

datatable_in.shape

datatable_out.shape

max(datatable_in['locprec-nm'])

max(datatable_in['outlier-score'])

plt.hist(datatable_in['outlier-score'])

max(datatable_out['locprec-nm'])

max(datatable_out['outlier-score'])

# ### Iterate over directory and save
# Not keeping every copy in memory as well, as sometimes work with large datasets

# #### Output directory

output_path = Path('C:/Nephrin_CODI-0079_2025-10-13/15nm_locs_outliers0-001')

# ### Filter and save

for counter, datatable_in in enumerate(datatables):
    datatable_out = datatable_in[datatable_in['locprec-nm'] < 15]
    datatable_out = datatable_out[datatable_out['outlier-score'] < 0.001]
    datatable_out.to_csv(output_path / (fovnames[counter] + '.csv'), index=False)



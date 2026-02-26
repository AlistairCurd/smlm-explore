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


rawdata_dirpath = Path("C:\\Collagen_CODI-0073_2026-02-24\\30nm_prec-p0-001\\locs")

# ## Load data
#
# ### Load tables from .csvs - downloaded using ONI API

# +
datatables = []
fovnames = []

for count, path_i in enumerate(rawdata_dirpath.iterdir()):
    if (count + 1) % 10 == 0:
        print(f'Dataset {count + 1} of {len(list(rawdata_dirpath.iterdir()))}...')
    datatable = pd.read_csv(
        path_i, skiprows=1, names=[
            'x-nm', 'y-nm', 'frame', 'channel', 'duration-frames', 'var-x-nm2', 'var-y-nm2', 'var-intensity-photons', 'var-background-photons',
            'var-sigma-x-nm2', 'var-sigma-y-nm2', 'z-nm', 'bg-mean-photons', 'sigma-x-mean-nm', 'sigma-y-mean-nm', 'intensity-mean-photons',
            'presplit-channels-channel-index', 'channel-group-index', 'parent-id', 'cluster-id', 'outlier-score', 'bleeding-distance-nm'
        ]
    )
    datatables.append(datatable)
    fovnames.append(path_i.stem)
print('Done all.')
# -

# ## Load tables from previously processed tables

# +
datatables = []
fovnames = []

for count, path_i in enumerate(rawdata_dirpath.iterdir()):
    if (count + 1) % 10 == 0:
        print(f'Dataset {count + 1} of {len(list(rawdata_dirpath.iterdir()))}...')
    datatable = pd.read_csv(
        path_i
    )
    datatables.append(datatable)
    fovnames.append(path_i.stem)
print('Done all.')
# -

# ### Check things are as expected

# #### Number of datasets in directory

len(datatables)

# #### Display a dataset

datatables[0]

# #### List the names of the datasets

fovnames

# ### Add localisation precision and average PSF sigma

for count, datatable in enumerate(datatables):
    if (count + 1) % 10 == 0:
        print(f'Dataset {count + 1} of {len(datatables)}...')    
    datatable['locprec-mean-nm'] = (np.sqrt(datatable['var-x-nm2']) + np.sqrt(datatable['var-y-nm2'])) / 2
    datatable['locprec-max-nm'] = np.sqrt(datatable[['var-x-nm2', 'var-y-nm2']]).max(axis=1)
    datatable['psf-sigma-mean-nm'] = (datatable['sigma-x-mean-nm'] + datatable['sigma-y-mean-nm']) / 2
print('Done.')

# ### Check again

datatables[0]

datatables[0][['var-x-nm2', 'var-y-nm2', 'locprec-mean-nm', 'locprec-max-nm']]

# ### Check localisation precision distribution for one fov

plt.hist(datatables[0]['locprec-max-nm'], bins=30, color='xkcd:sea green')
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

"C:\\Autofluorescence-CRC-CODI-92_2025-11-11\\50nm_locs-p0-05\\NaBH4_blank"
,"C:\\Autofluorescence-CRC-CODI-92_2025-11-11\\50nm_locs-p0-05\\no-quencher_blank"
,"C:\\Autofluorescence-CRC-CODI-92_2025-11-11\\50nm_locs-p0-05\\alc-amm-blank"
,"C:\\Autofluorescence-CRC-CODI-92_2025-11-11\\50nm_locs-p0-05\\amm-chl_blank"
,"C:\\Autofluorescence-CRC-CODI-92_2025-11-11\\50nm_locs-p0-05\\amm-chl_NaBH4_blank"
,"C:\\Autofluorescence-CRC-CODI-92_2025-11-11\\50nm_locs-p0-05\\amm-chl-1hr-blank"
,"C:\\Autofluorescence-CRC-CODI-92_2025-11-11\\50nm_locs-p0-05\\Invitrogen-blank"
    
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
# plt.ylim((0, 200000))
plt.savefig('C:/Temp/numbers-of-locs-by-autofl-quenching-method.pdf', bbox_inches='tight')
plt.show()

plt.scatter(fovs_summary_df['condition'], fovs_summary_df['num_locs'], s=5)
plt.xticks(rotation=90)
plt.show()

plt.scatter(fovs_summary_df['condition'], fovs_summary_df['num_locs'], s=5)
plt.xticks(rotation=90)
plt.ylim([0, 200000])
plt.show()

# ## Plot localisation parameter distributions

# One row for each condition, localisation precision and PSF size

# +
fig, axes = plt.subplots(len(datadir_paths_list), 4, figsize=(11, 13), layout='constrained', sharex=False)

ylim = [0, 20000]
xlim_psf = [0, 200]

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
        axes[row, 1].set_ylim(*ylim)
        

        psf_hist_values_locsto30nm, edges = np.histogram(datatable['psf-sigma-nm'][datatable['locprec-nm'] < 30], bins=30)
        bin_centres = (edges[0:-1] + edges[1:]) / 2
        axes[row, 2].plot(bin_centres, psf_hist_values_locsto30nm)
        axes[row, 2].set_xlim(*xlim_psf)
        axes[row, 2].set_ylim(*ylim)

        psf_hist_values_locsto15nm, edges = np.histogram(datatable['psf-sigma-nm'][datatable['locprec-nm'] < 15], bins=30)
        bin_centres = (edges[0:-1] + edges[1:]) / 2
        axes[row, 3].plot(bin_centres, psf_hist_values_locsto15nm)
        axes[row, 3].set_xlim(*xlim_psf)
        axes[row, 3].set_ylim(0, 6000)

        axes[row, 0].set_ylabel(rawdata_dirpath.stem[0:-6], rotation=90)

axes[len(datadir_paths_list) - 1, 0].set_xlabel('loc-prec (nm)')
axes[len(datadir_paths_list) - 1, 1].set_xlabel('PSF sigma (nm)')
axes[len(datadir_paths_list) - 1, 2].set_xlabel('PSF sigma (nm) (prec < 30 nm)')
axes[len(datadir_paths_list) - 1, 3].set_xlabel('PSF sigma (nm) (prec < 15 nm)')


# -

fig.savefig('C:/Temp/locprec-and-psf-various-autofl-conditions.pdf', bbox_inches='tight')

# # Filter data

# ### Test/check on one FOV

datatables[0].columns

max(datatables[0]['locprec-mean-nm'])

# +
#Test

datatable_in = datatables[10]
datatable_out = datatable_in[datatable_in['locprec-max-nm'] < 15]
datatable_mean_thresh = datatable_in[datatable_in['locprec-mean-nm'] < 15]
# datatable_out = datatable_out[datatable_out['outlier-score'] < 0.001]
# -

datatable_in.shape

datatable_out.shape

datatable_mean_thresh.shape

max(datatable_in['locprec-max-nm'])

max(datatable_in['outlier-score'])

plt.hist(datatable_in['outlier-score'])

max(datatable_out['locprec-max-nm'])

max(datatable_out['outlier-score'])

max(datatable_mean_thresh['locprec-mean-nm'])

max(datatable_mean_thresh['locprec-max-nm'])

plt.hist(datatable_mean_thresh['locprec-mean-nm'])

# ### Iterate over directory and save
# Not keeping every copy in memory as well, as sometimes work with large datasets

# #### Output directory

output_path = Path("C:/Collagen_CODI-0073_2026-02-24/15nm-precxymean_p001/locs")
if not output_path.exists():
    output_path.mkdir(parents=True, exist_ok=False)

# ### Filter and save

for count, datatable_in in enumerate(datatables):
    if (count + 1) % 10 == 0:
        print(f'Dataset {count + 1} of {len(datatables)}...')
    datatable_out = datatable_in[datatable_in['locprec-mean-nm'] < 15]
    max_prec = datatable_out['locprec-mean-nm'].max()
    if max_prec > 15:
        print(f'{fovnames[count]}: {max_prec} nm')
    # datatable_out = datatable_out[datatable_out['outlier-score'] < 0.001]
    datatable_out.to_csv(output_path / (fovnames[count] + '.csv'), index=False)
print('Done.')



# + active=""
#

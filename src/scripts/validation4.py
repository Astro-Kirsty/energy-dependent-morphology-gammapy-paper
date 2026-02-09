import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2, norm
import pandas as pd
from astropy.table import Table
import paths

table = Table.read(paths.data / 'results_3Eband_simulated.csv')
delta_ts = np.array(table['delta_ts'])
delta_ts = delta_ts[np.isfinite(delta_ts)]
significance = np.array(table['significance'])
df = table['dof'][0]
num_energy_bands = sum(col.endswith('_lon_0') and col.startswith('slice') for col in table.columns)
cb_color1 = '#0072B2' 
N = 3 

def chi2_parameters(parameter):
    chi2_values = []
    for ii in range(len(table)):
        param = np.array([table[f'slice{i}_{parameter}'][ii] for i in range(num_energy_bands)])
        param_errs = np.array([table[f'slice{i}_{parameter}_err'][ii] for i in range(num_energy_bands)])
        weight = 1 / param_errs**2
        avg = np.average(param, weights=weight)
        chi2_values += [ np.sum( (param-avg)**2 / param_errs**2) ]
    chi2_values = np.array(chi2_values)
    return chi2_values[np.isfinite(chi2_values)]
    
params =  ["sigma", "lon_0", "lat_0"]

chi2_values = np.column_stack([chi2_parameters(p) for p in params])
maximums = np.amax(chi2_values, axis=1)
df_chi2 = num_energy_bands - 1

#--------------- Figure 9 -----------------
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(5, 13))
p_value_chi2 = 1 - chi2.cdf(maximums, df=df_chi2)**N
p_value_deltats = chi2.sf(delta_ts, df=6)
sig_chi2 = norm.isf(0.5 * p_value_chi2)
sig_deltats = np.sqrt(chi2.isf(p_value_deltats, df=1))
data = [
    (maximums, delta_ts, '$\max(\chi_p^2)$', '$\Delta$TS'),
    (p_value_chi2, p_value_deltats, 'p-value ($\max(\chi_p^2)$)', 'p-value ($\Delta$TS)'),
    (sig_chi2, sig_deltats, 'Significance ($\max(\chi_p^2)$)', 'Significance ($\Delta$TS)')
]
for ax, (x, y, xlabel, ylabel) in zip(axes, data):
    ax.plot(x, y, 'o', color=cb_color1, alpha=0.4)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
        
axes[1].plot([min(p_value_chi2), max(p_value_chi2)], [min(p_value_chi2), max(p_value_chi2)], 
             ls='--', color='black', linewidth=1.5, label='$x=y$')

axes[2].plot([min(sig_chi2), max(sig_chi2)], [min(sig_chi2), max(sig_chi2)], 
             ls='--', color='black', linewidth=1.5, label='$x=y$')
fig.savefig(paths.figures / 'sensitivity_3ebands.pdf', bbox_inches='tight')        





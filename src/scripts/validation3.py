import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2
import pandas as pd
from astropy.table import Table
import paths

table = Table.read(paths.data / 'results_3Eband_simulated.csv')
delta_ts = np.array(table['delta_ts'])
delta_ts = delta_ts[np.isfinite(delta_ts)]
num_energy_bands = sum(col.endswith('_lon_0') and col.startswith('slice') for col in table.columns)
cb_color1 = '#0072B2' 
cb_color2 = '#D55E00'

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
N = 3     

#--------------- Figure 8 -----------------
fig, ax = plt.subplots(figsize=(5, 3.75))
values, bins, _ = ax.hist(maximums, bins=40, density=True, color=cb_color1,
                          label=f'Simulations={len(delta_ts)}',
                          edgecolor='black', alpha=0.4)
P_eqn = N * chi2.pdf(bins, df_chi2) * (chi2.cdf(bins, df_chi2))**(N-1)
ax.plot(bins, P_eqn, color=cb_color2, linestyle='--', linewidth=2)
ax.text(0.5, 0.9, 'Values for P function', verticalalignment='bottom', fontsize=11, 
        transform=ax.transAxes, horizontalalignment='left', color=cb_color2, fontweight='bold')
ax.text(0.5, 0.885, f'Energy bands={num_energy_bands} \ndf = {df_chi2} \nN = {N}', fontsize=11,  
        verticalalignment='top', transform=ax.transAxes, horizontalalignment='left')
ax.set_ylabel('Probability Density', fontsize=11)
ax.set_xlabel(f'$\max(\chi_p^2)$', fontsize=11)
for spine in ax.spines.values():
    spine.set_linewidth(1.5)
fig.savefig(paths.figures / 'chi2_maximums_3ebands.pdf', bbox_inches='tight')        






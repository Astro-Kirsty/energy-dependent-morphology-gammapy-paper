import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2
import pandas as pd
from astropy.table import Table
import paths

paths.figures.mkdir(parents=True, exist_ok=True)

table = Table.read(paths.data / 'results_3Eband_simulated.csv')
delta_ts = np.array(table['delta_ts'])
delta_ts = delta_ts[np.isfinite(delta_ts)]
df = table['dof'][0]
cb_color1 = '#0072B2' 
cb_color2 = '#D55E00'


#--------------- Figure 6 -----------------
fig, ax = plt.subplots(figsize=(5, 3.75))
values, bins, _ = ax.hist(delta_ts, bins=40, density=True, color=cb_color1, label=f'Simulations={len(delta_ts)}',
                          edgecolor='black', alpha=0.4)
centers = 0.5*(bins[:-1]+bins[1:])
ax.set_ylabel('Probability Density', fontsize=11)
ax.set_xlabel('$\Delta$TS', fontsize=11)
ax.plot(centers, chi2.pdf(centers, df=df), color=cb_color2, linestyle='--', linewidth=2)
ax.legend(loc='upper right', fontsize=11)
ax.text(0.5, 0.78, 'Expected $\\chi^2$ function', verticalalignment='bottom',
        transform=ax.transAxes, horizontalalignment='left', color=cb_color2, fontweight='bold', fontsize=11)
ax.text(0.5, 0.78, f'df = {df}',  
        verticalalignment='top', transform=ax.transAxes, horizontalalignment='left', fontsize=11)
for spine in ax.spines.values():
    spine.set_linewidth(1.5) 
fig.savefig(paths.figures / 'deltaTS_mock_3ebands.pdf', bbox_inches='tight')              





import numpy as np
from astropy import units as u
from astropy.table import Table
import matplotlib.pyplot as plt
import matplotlib
import paths

table = Table.read(paths.data / 'edep_results_alpha0.3_sigma0.1.dat', format='ascii')
alpha0, sigma0 = 0.3, 0.1
energy = np.logspace(-1, 2, 10)*u.TeV

e_min, e_max = table['Emin'][1:], table['Emax'][1:]
e_center = np.sqrt(e_min * e_max)
e_err = [e_center - e_min, e_max - e_center]

sigma = table['sigma'][1:]
sigma_err = table['sigma_err'][1:]

def expected_function(energy, sigma, alpha):
    return sigma * energy**(-alpha)

fig, ax = plt.subplots(figsize=(5, 3.75))
ax.errorbar(e_center, sigma, fmt='None', xerr=e_err, yerr=sigma_err, 
             label='Estimator result', color='#0072B2', alpha=0.9)

ax.plot(energy[1:], expected_function(energy[1:], sigma0, alpha0), color='grey', ls='--', alpha=0.8, label='Expected')

ax.set_xscale('log')
ax.set_xlabel('Energy (TeV)')
ax.set_ylabel('Extension')
ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%1.2f$^\\mathrm{o}$'))
ax.legend()
fig.savefig(paths.figures / 'spatial_example2_curve.pdf', bbox_inches='tight')

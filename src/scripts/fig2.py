from gammapy.maps import Map
import matplotlib.patheffects as pe
from matplotlib.patches import Circle
from astropy.coordinates import SkyCoord
from astropy import units as u
import matplotlib.pyplot as plt
import paths

#significance_cutout = Map.read(paths.data / 'significance_map_J1825.fits')
significance_cutout = Map.read('../data/significance_map_J1825.fits')
PSR_position = SkyCoord(l=18.00018*u.deg, b=-0.69093*u.deg, frame='galactic')

def add_psr(ax, color='mediumturquoise'):
    psr_region = Circle((PSR_position.l.value, PSR_position.b.value), 0.05,
                    transform=ax.get_transform('galactic'), 
                    edgecolor='black', facecolor=color)
    ax.add_patch(psr_region)
    
    ax.text(19.35, -1, 'PSR B1823-13', fontweight='bold', fontsize=10, 
            path_effects=[pe.withStroke(linewidth=1.5, foreground="black")],
            transform=ax.get_transform('galactic'), zorder=12, color=color)
            
def galactic_plotting(ax, lat_on=True, lon_on=True, tickspacing=1*u.deg, color='white',
            formatter='d'):
    """Format the axes as galactic coordinates."""
    lon, lat = ax.coords[0], ax.coords[1]
    lon.set_axislabel('Galactic Longitude')
    lat.set_axislabel('Galactic Latitude')
    lat.set_major_formatter(formatter)
    lon.set_major_formatter(formatter)

    lon.set_ticklabel_visible(lon_on)
    lat.set_ticklabel_visible(lat_on)

    lon.set_ticks(spacing=tickspacing, color=color)
    lat.set_ticks(spacing=tickspacing, color=color)
    lon.display_minor_ticks(True) 
    lon.set_minor_frequency(4)
    lat.display_minor_ticks(True)
    lat.set_minor_frequency(4)
    
    ax.tick_params(direction='in')

    return ax
    
lon_flags = [False, False, True] 
energy_labels = ['0.4 - 2 TeV', '2 - 10 TeV', '10 - 100 TeV']
vmax_values = [20, 15, 8]

fig, axes = plt.subplots(3, 1, figsize=(6, 12),
                         subplot_kw={"projection": significance_cutout.geom.wcs},
                         gridspec_kw={"left": 0.1, "right": 0.9})

for ax, data, vmax, label, lon_on in zip(axes, significance_cutout.data, vmax_values, energy_labels, lon_flags):
    img = ax.imshow(data, cmap=plt.cm.afmhot, vmin=-2, vmax=vmax, rasterized=True)
    cb = fig.colorbar(img, ax=ax, pad=0.005)
    cb.ax.locator_params(nbins=5)
    cb.set_label('Significance ($\sigma$)', rotation=270, labelpad=15)
    ax.text(0.05, 0.93, f'Energy {label}', transform=ax.transAxes,
            color='white', fontsize=12, fontweight='bold')
    
    galactic_plotting(ax, lon_on=lon_on)
    
    add_psr(ax)
    
fig.subplots_adjust(hspace=0.03)
fig.savefig(paths.figures / 'dataset_ebands.pdf', bbox_inches='tight')

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.table import Table
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from gammapy.modeling.models import GaussianSpatialModel
from gammapy.maps import Map
from regions import CircleSkyRegion, LineSkyRegion
import paths

def galactic_plotting(ax, lat_on=True, lon_on=True, tickspacing=0.7*u.deg, color='black',
            formatter='d.d'):
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
    
    
table_edep = Table.read(paths.data / 'edep_results_J1825.dat', format='ascii')
source_position = SkyCoord(l=17.5252, b=-0.6177, frame='galactic', unit='deg')
empty_map = Map.create(
    skydir=source_position, frame='galactic', width=2.5, binsz=0.02
)

PSR_position = SkyCoord(l=18.00018*u.deg, b=-0.69093*u.deg, frame='galactic')

colors = ['#6A3D9A', '#009E73', '#E69F00']    

fig = plt.figure(figsize=(6, 4))
ax = empty_map.plot(cmap='Greys')

for i, row in enumerate(table_edep[1:]):
    lat_0 = row['lat_0'] * u.deg
    lon_0 = row['lon_0'] * u.deg
    sigma = row['sigma'] * u.deg

    lat_err = row['lat_0_err'] * u.deg
    lon_err = row['lon_0_err'] * u.deg
    sigma_err = row['sigma_err'] * u.deg

    # Create Gaussian model
    model = GaussianSpatialModel(lat_0=lat_0, lon_0=lon_0, sigma=sigma, frame='galactic')
    model.lat_0.error = lat_err
    model.lon_0.error = lon_err
    model.sigma.error = sigma_err

    # Plot model and errors
    ax.add_artist(model.to_region().to_pixel(ax.wcs).as_artist(color=colors[i]))
    model.plot_error(ax=ax, which="extension",
                     kwargs_extension={"facecolor": colors[i], "edgecolor": colors[i], "alpha": 0.4})

    # Plot position error 
    lat_line = LineSkyRegion(
        start=SkyCoord(lon_0, lat_0 - 2*lat_err, frame='galactic'),
        end=SkyCoord(lon_0, lat_0 + 2*lat_err, frame='galactic')
    )
    ax.add_artist(lat_line.to_pixel(ax.wcs).as_artist(color=colors[i], alpha=0.6))
    lon_line = LineSkyRegion(
        start=SkyCoord(lon_0 - 2*lon_err, lat_0, frame='galactic'),
        end=SkyCoord(lon_0 + 2*lon_err, lat_0, frame='galactic')
    )
    ax.add_artist(lon_line.to_pixel(ax.wcs).as_artist(color=colors[i], alpha=0.6))
    
    # Plot energy bands
    if row['Emin']<1:
        ax.text(0.5, 1.17-(i*0.07), 
                r'$\mathbf{E_{%d} = %.1f - %.0f\, TeV}$' % (i + 1, row['Emin'], row['Emax']),
                transform=ax.transAxes, fontsize=12, color=colors[i], horizontalalignment='center')  
    else:
        ax.text(0.5, 1.17-(i*0.07), 
            r'$\mathbf{E_{%d} = %.0f - %.0f\, TeV}$' % (i + 1, row['Emin'], row['Emax']),
            transform=ax.transAxes, fontsize=12, color=colors[i], horizontalalignment='center')  

galactic_plotting(ax)

ax.text(0.5, 1.25, 'Energy bands', transform=ax.transAxes, fontsize=12, color='black', fontweight='bold',
       horizontalalignment='center')

ax.add_patch(Circle((PSR_position.l.deg, PSR_position.b.deg), 0.01, transform=ax.get_transform('galactic'), 
            edgecolor='black', lw=3, facecolor='black'))
ax.text(0.1, 0.05, 'PSR B1823-13', fontweight='bold', fontsize=13, 
        transform=ax.transAxes, zorder=12, color='black')
ax.arrow(18., -1.6, 0., 0.75, fc='black',ec='black',clip_on=False, head_width=0.06, 
         transform=ax.get_transform('galactic'))

position = SkyCoord(l=16.45*u.deg, b=-1.7*u.deg, frame='galactic')
circle = CircleSkyRegion(center=position, radius=0.07*u.deg)
ax.add_artist(circle.to_pixel(ax.wcs).as_artist())
ax.text(16.48, -1.57, 'PSF', transform=ax.get_transform('galactic'), 
        horizontalalignment='center', fontweight='bold')
fig.savefig(paths.figures / 'spatial_3ebands.pdf', bbox_inches='tight')        

from astropy import units as u
from astropy.coordinates import SkyCoord
from IPython.display import display
from gammapy.datasets import MapDataset, Datasets
from gammapy.modeling.models import (
    GaussianSpatialModel,
    PowerLawSpectralModel,
    SkyModel,
)
from gammapy.estimators import EnergyDependentMorphologyEstimator

dataset = MapDataset.read(
    "dataset_energy_dependent.fits.gz"
)
datasets = Datasets([dataset])
energy_edges = [0.3, 2, 10, 100] * u.TeV

src_pos = SkyCoord(21.5, -0.89, unit="deg", frame="galactic")
spectral_model = PowerLawSpectralModel(
    index=2.4, 
    amplitude=4.22e-13 * u.Unit("cm-2 s-1 TeV-1"), 
    reference=1.0 * u.TeV,
)
spatial_model = GaussianSpatialModel(
    lon_0=src_pos.l,
    lat_0=src_pos.b,
    frame="galactic",
    sigma=0.2 * u.deg,
)

# Limit the search for the position on the spatial model
spatial_model.lon_0.min = src_pos.galactic.l.deg - 0.8
spatial_model.lon_0.max = src_pos.galactic.l.deg + 0.8
spatial_model.lat_0.min = src_pos.galactic.b.deg - 0.8
spatial_model.lat_0.max = src_pos.galactic.b.deg + 0.8

model = SkyModel(
    spatial_model=spatial_model, 
    spectral_model=spectral_model, 
    name="src",
)
model.spectral_model.index.frozen = True
datasets.models = model

estimator = EnergyDependentMorphologyEstimator(
    energy_edges=energy_edges, 
    source="src",
)

results = estimator.run(datasets)
results_edep = results["energy_dependence"]
display(results_edep["result"])
print(f"df = {results_edep['df']}")
print(f"deltaTS = {results_edep['delta_ts']}")
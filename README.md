<p align="center">
<br>
<a href="https://github.com/Astro-Kirsty/energy-dependent-morphology-gammapy-paper/actions/workflows/build.yml">
<img src="https://github.com/Astro-Kirsty/energy-dependent-morphology-gammapy-paper/actions/workflows/build.yml/badge.svg?branch=main" alt="Article status"/>
</a>
<a href="https://github.com/Astro-Kirsty/energy-dependent-morphology-gammapy-paper/raw/main-pdf/arxiv.tar.gz">
<img src="https://img.shields.io/badge/article-tarball-blue.svg?style=flat" alt="Article tarball"/>
</a>
<a href="https://github.com/Astro-Kirsty/energy-dependent-morphology-gammapy-paper/raw/main-pdf/ms.pdf">
<img src="https://img.shields.io/badge/article-pdf-blue.svg?style=flat" alt="Read the article"/>
</a>
</p>


# "Energy-dependent gamma-ray morphology estimation tool in Gammapy" paper

This repository is for the reproducability of the paper titled above.

The paper was accepted to [Astronomy and Astrophysics](https://www.aanda.org/).
This is an open access paper available at [doi:10.1051/0004-6361/202555208](https://doi.org/10.1051/0004-6361/202555208).

## To build the paper locally:

First you need to fork this repo and clone it to your local machine:

    git clone https://github.com/yourgithub/energy-dependent-morphology-gammapy-paper.git
    
Then you can create and activate the conda environment there:

    conda env create -f environment.yml
    conda activate edep-syw-paper
    
Finally, you can user `showyourwork` to build the paper and figures:

    showyourwork build


This version of the paper is open source and was created using the [showyourwork](https://github.com/showyourwork/showyourwork) workflow.

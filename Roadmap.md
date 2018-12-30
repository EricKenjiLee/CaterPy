#Development Roadmap
This file is meant to serve as a roadmap of developing this package into version 1.0.0 and will specify the project's
structure, class structure, features, API, etc. The package should be written such that it is agnostic to the data type.

##Ground Rules
1) Documentation should be written in reStructured text and documentation generated in Sphinx pushed to Github pages.
2) Linting should be run at every commit to any branch
3) Tests should be written using PyTest and a suite of tests should be run using a pre-merge hook between 
`development` and `master` branches. Coverage should be calculated and displayed as a button in the README.
4) Continuous integration tests should be run after every commit to `master` using CircleCI. This to check package 
compatibilities.

##Class Structure
- TimeSeries: this np.array object can receive a variety of data types and will convert them to a single type. Preprocessing 
(standardization/normalization/centering/whitening) will occur at this step.
- SSA(TimeSeries\[:,i\]): this object receives a single (n x 1) time-series and can conduct the four steps outlined in Golyandina et al.
- MSSA(TimeSeries\[:,:\]): this object receives an array (n x n) of time series's and conducts the stages of processing in Andreas Groth's work
- TSSA(TimeSeries\[:,i\]): this object will receive a single (n x 1) time-series and generate a tensor from the Toeplitz matrix. Computation is as 
follows from Kouchaki et al.
- CPSSA(TimeSeries\[:,:\]): a decomposition of a matrix (n x n) using a CP-decomposition that currently doesn't 
appear in the literature. Using original code, TensorLy, or TensorTools.

## Scope
1) single-channel singular spectrum analysis
2) multivariate singular spectrum analysis
3) tensor singular spectrum analysis
4) statistical significance testing framework

## Initial Datasets
- Standard climate dataset (SSA)
- Bristol Bay Fisheries dataset (MSSA)
- Narrow-field calcium imaging data set from the Allen Brain Observatory (MSSA)

## Future Datasets
- CNMF processed Mesoscope imaging
- multi-area simultaneous Neuropixels recordings
 
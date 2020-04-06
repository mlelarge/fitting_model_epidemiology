# Estimating models in epidemiology with optimization

This repo describes a method to find parameters for a SIR like model from a partial view of the trajectory (i.e. with hidden variables).

<p align="center">
  <img width="500" src="https://github.com/mlelarge/fitting_model_epidemiology/blob/master/images/fit_synth.png">
</p>


If we have only access to the number of individuals in hospital (dashed green curve above) and the number of deceased individuals (dashed red curve above) as a function of time, we can still estiamte the number of infectious individuals as shown in the picture above. The estimated number of infectious individuals is given in blue and the true number of infectious individuals (as given by our synthetic model) is given in dashed blue.

The problem and the method is described in the [Synthetic_data](https://github.com/mlelarge/fitting_model_epidemiology/blob/master/Synthetic_data.ipynb) notebook and its application to real data is done in the [Real data](https://github.com/mlelarge/fitting_model_epidemiology/blob/master/Real_data.ipynb)

Author: [Marc Lelarge](https://www.di.ens.fr/~lelarge/)

# The impact of contact tracing: simulation study

I am puzzled by the fact that the current debate around a possible tracking app is focusing on the privacy issue instead of its relevance for containing the virus. We are ready to give our geolocation data to avoid a traffic jam but not to save lives!

There are quite a few limitations to the current proposals for contact tracing as it is very well explained by Ross Anderson in [Contact Tracing in the Real World](https://www.lightbluetouchpaper.org/2020/04/12/contact-tracing-in-the-real-world/). But technology will probably play a crucial role if it is shown to be efficient and if public trust it.

Here I try to explain the impact of contact tracing on a simple model through simulations. 

Here is an html version of the study [Impact_tracing_simulation](https://rawcdn.githack.com/mlelarge/fitting_model_epidemiology/b2ecb32383169e888ea9e7bdf64785b1846d465a/Impact_tracing_simulation.html)

Code is available here: [Impact_tracing_simulation](https://github.com/mlelarge/fitting_model_epidemiology/blob/master/Impact_tracing_simulation.ipynb)

# Estimating models in epidemiology with optimization

This repo describes a method to find parameters for a SIR like model from a partial view of the trajectory (i.e. with hidden variables).

<p align="center">
  <img width="500" src="https://github.com/mlelarge/fitting_model_epidemiology/blob/master/images/fit_synth.png">
</p>


For example, if we have only access to the number of individuals in hospital (dashed green curve above) and the number of deceased individuals (dashed red curve above) as a function of time, we can still estimate the number of infectious individuals as shown in the picture above. The estimated number of infectious individuals is given in blue and the true number of infectious individuals (as given by our synthetic model) is given in dashed blue.

The problem and the method is described in the [Synthetic_data](https://github.com/mlelarge/fitting_model_epidemiology/blob/master/Synthetic_data.ipynb) notebook and its application to real data is done in the [Real data](https://github.com/mlelarge/fitting_model_epidemiology/blob/master/Real_data.ipynb)

Here is an html version of [Synthettic data](https://rawcdn.githack.com/mlelarge/fitting_model_epidemiology/370951067f45c183f23a929d7e02bce91e608da0/Synthetic_data.html)

Author: [Marc Lelarge](https://www.di.ens.fr/~lelarge/)

# Disclaimer

I am an applied mathematician, not an epidemiologist. The main purpose of this repository is to test ideas but they need to be validated by an expert. There are still problems with the model but I think it can be fixed with your help!

Please use the code in this repository with care.

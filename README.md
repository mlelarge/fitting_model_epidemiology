# Estimating models in epidemiology with optimization

This repo describes a method to find parameters for a SIR like model.

The problem can be described as follows: we are given a familly of ODEs $y'=h_\\theta(y,t)$, where the function $h$ is parametrized by the parameter $\\theta$ and a trajectory $z$, the problem is to find the best value of $\\theta$ such that $z'\\approx h_{\\theta}(z,t)$. In order to find the value of $\\theta$, we follow an optimization approach based on the tool developed in [Neural Ordinary Differential Equations](https://arxiv.org/abs/1806.07366). Namely, for a distance function $D$ on $\\mathbb{R}^d$, we define $L = D(y_\\theta -z)$ where $y_\\theta$ is the solution of the ODE $y'=h_{\\theta}(y,t)$ and we minimize the loss $L$ with respect to $\\theta$ with SGD.

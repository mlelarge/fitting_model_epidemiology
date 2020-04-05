import numpy as np
import pandas as pd

import torch
import torch.nn as nn
import torch.optim as optim
from torchdiffeq import odeint

class IHD_model(nn.Module):
    def __init__(self,parms,time):
        super(IHD_model,self).__init__()
        self.b1 = torch.nn.Parameter(parms[0])
        self.b2 = torch.nn.Parameter(parms[1])
        self.g = torch.nn.Parameter(parms[2])
        self.nu = torch.nn.Parameter(parms[3])
        self.l = torch.nn.Parameter(parms[4])
        self.time = torch.nn.Parameter(time)
        self.m = torch.nn.Sigmoid()

    def forward(self, t, y):
        b = self.b1 + self.b2*(self.m(t-self.time))
        I,H,D = y[:,0], y[:,1], y[:,2]
        dI = b*I-self.g*I-self.nu*I
        dH = self.nu*I-self.g*H-self.l*H
        dD = self.l*H
        return torch.cat((dI,dH,dD),0)

class IHD_fit(nn.Module):
    def __init__(self,parms):
        super(IHD_fit,self).__init__()
        self.b = torch.nn.Parameter(parms[0])
        self.g = torch.nn.Parameter(parms[1])
        self.nu = torch.nn.Parameter(parms[2])
        self.l = torch.nn.Parameter(parms[3])
        
    def forward(self,t,y):
        I,H,D = y[:,0], y[:,1], y[:,2]
        dI = self.b*I-self.g*I-self.nu*I
        dH = self.nu*I-self.g*H-self.l*H
        dD = self.l*H
        return torch.cat((dI,dH,dD),0)        

class IHD_fit_time(nn.Module):
    def __init__(self,parms, time):
        super(IHD_fit_time,self).__init__()
        self.b1 = torch.nn.Parameter(parms[0])
        self.b2 = torch.nn.Parameter(parms[1])
        self.g = torch.nn.Parameter(parms[2])
        self.nu = torch.nn.Parameter(parms[3])
        self.l = torch.nn.Parameter(parms[4])
        self.time = torch.nn.Parameter(time)
        self.m = torch.nn.Sigmoid()
        
    def forward(self,t,y):
        I,H,D = y[:,0], y[:,1], y[:,2]
        b = self.b1 + self.b2*self.m(t-self.time)
        dI = b*I-self.g*I-self.nu*I
        dH = self.nu*I-self.g*H-self.l*H
        dD = self.l*H
        return torch.cat((dI,dH,dD),0)

def predic_ode(model,init, t):
    with torch.no_grad():
        true_y = odeint(model, init, t, method='dopri5')
    return true_y.squeeze(1)

def trainig(model, init, t, optimizer,criterion,niters,data,all_data = True):
    best_loss = 1000.
    parms_best = model.parameters()
    for itr in range(1, niters + 1):
        optimizer.zero_grad()
        pred_y = odeint(model,init, t)
        if all_data:
            loss = criterion(pred_y.squeeze(1),data)
        else:
            loss = criterion(pred_y[:,0,0],data[0])+criterion(pred_y[:,0,2],data[1])
        loss.backward()
        optimizer.step()
        if loss.item() < best_loss:
            best_loss = loss.item()
            parms_best = model.parameters()
        if itr% 10 ==0:
            print(itr,loss.item(),[p.data for p in model.parameters()])
    return best_loss, list(parms_best)

def get_best_model(l):
    parms_inf = torch.cat([p.data.unsqueeze(0) for p in l[:-1]],0)
    time_inf = l[-1].data
    return IHD_fit_time(parms_inf,time_inf)

def get_best_model_simple(l):
    parms_inf = torch.cat([p.data.unsqueeze(0) for p in l],0)
    return IHD_fit(parms_inf)
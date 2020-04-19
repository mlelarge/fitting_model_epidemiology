from simulation_tracing import Simu
import numpy as np

all_time_test = np.arange(10,80,5)
n_time_test = len(all_time_test)
n_simu = 150
n = 1000
n_time = 300

def make_one_simu(time_test):
    simu = Simu(n=n, n_time=n_time,p_contact=0,time_test=time_test)
    simu.make_simu_test()
    infected = simu.all_infected()
    susceptible = simu.all_susceptible()
    symptoms = simu.all_symptoms()
    recovered = simu.all_last()
    p_infected = simu.all_protected_infected()
    p_susceptible = simu.all_protected_susceptible()
    p_symptoms = simu.all_protected_symptoms()
    p_recovered = simu.all_protected_last()
    return infected, susceptible, symptoms, recovered, p_infected, p_susceptible, p_symptoms, p_recovered

all_infected = np.zeros((n_simu,n_time_test,n_time))
all_susceptible = np.zeros((n_simu,n_time_test,n_time))
all_symptoms = np.zeros((n_simu,n_time_test,n_time))
all_recovered = np.zeros((n_simu,n_time_test,n_time))
all_p_infected = np.zeros((n_simu,n_time_test,n_time))
all_p_susceptible = np.zeros((n_simu,n_time_test,n_time))
all_p_symptoms = np.zeros((n_simu,n_time_test,n_time))
all_p_recovered = np.zeros((n_simu,n_time_test,n_time))

for j,time_test in enumerate(all_time_test):
    print('start simu for time test', time_test)
    for i in range(n_simu):
        print('start simu', i)
        infected, susceptible, symptoms, recovered, p_infected, p_susceptible, p_symptoms, p_recovered = make_one_simu(time_test)
        all_infected[i,j,:] = infected
        all_susceptible[i,j,:] = susceptible
        all_symptoms[i,j,:] = symptoms
        all_recovered[i,j,:] = recovered
        all_p_infected[i,j,:] = p_infected
        all_p_susceptible[i,j,:] = p_susceptible
        all_p_symptoms[i,j,:] = p_symptoms
        all_p_recovered[i,j,:] = p_recovered

data = [all_infected, all_susceptible, all_symptoms, all_recovered, all_p_infected, all_p_susceptible, all_p_symptoms, all_p_recovered]

np.savez('data100_test.npz', *data)
    

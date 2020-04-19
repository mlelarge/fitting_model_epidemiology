import numpy as np
from scipy import spatial

#SIMULATION PARAMETERS
p_init = 0.05  #fraction of infected people at the beginning of the simulation
r_cont = 3  #radius of transmission in pixels (0-100)
p_cont = 0.6  #probability of transmission
p_heal = 0.8 #propa recovering not used!
time_test = 50 #time between 2 tests
p_contact = 1 #fraction with tracing app
end_time_low = 90   #low time taken to recover in number of frames (0-infinity)
end_time_high = 110   #high time taken to recover in number of frames (0-infinity)
detec_time_low = 20 #low time taken to see symptoms
detec_time_high = 50 #high time taken to see symptoms
delta_time = 50 #  history for the list of contacts (number of frames)
time_protected = 50 # time in isolation when signal (number of frames)

class Simu:
    def __init__(self, n, n_time, p_init = p_init,
            p_cont=p_cont, p_heal=p_heal, r_cont=r_cont,
            delta_time =  delta_time, p_contact= p_contact,
            end_time_low=end_time_low, end_time_high = end_time_high, 
            detec_time_low = detec_time_low, detec_time_high = detec_time_high, time_protected=time_protected, time_test=time_test):
        self.n = n # number of individuals
        self.n_time = n_time # number of times in simulation
        self.p_init = p_init
        self.p_cont = p_cont
        self.p_heal = p_heal
        self.p_contact = p_contact
        self.r_cont = r_cont
        self.time_protected = time_protected
        self.time_test = time_test
        self.indices = [(int(k*self.n/self.time_test), int((k+1)*self.n/self.time_test) ) for k in range(self.time_test)]
        self.n_indices = len(self.indices)
        self.delta_time = delta_time
        self.end_time_low = end_time_low
        self.end_time_high = end_time_high
        self.detec_time_low = detec_time_low
        self.detec_time_high = detec_time_high
        self.n_time = n_time
        self.init_pop_param()
        self.init_pop()
        self.tensor_contact = np.zeros((self.n,self.n,self.n_time))
        self.tensor_contact[:,:,0] = self.make_contact_matrix(0)
        
    def init_pop_param(self, n_param = 6):
        # detection_time, end_time, rec/dead, speed, init_infected, contact tracing
        self.n_param = n_param
        self.pop_param = np.zeros((self.n,self.n_param))
        self.pop_param[:,0] = np.random.randint(self.detec_time_low,self.detec_time_high+1,self.n)
        self.pop_param[:,1] = np.random.randint(self.end_time_low,self.end_time_high+1,self.n)
        self.pop_param[:,2] = np.random.choice([0,1],size=self.n,p=[self.p_heal,1-self.p_heal])
        self.pop_param[:,3] = np.ones(self.n)*0.5
        self.pop_param[:,4] = np.random.choice([0,1],size = self.n , p = [1-self.p_init, self.p_init] )
        self.pop_param[:,5] = np.random.choice([0,1],size = self.n , p = [1-self.p_contact, self.p_contact] )

    def init_pop(self, n_dyn=11):
        # S, I, Sy, L, posx, posy, destx, desty, infec_time, protected, protec_time
        self.pop_dyn = np.zeros((self.n,self.n_time,n_dyn))
        self.pop_dyn[:,0,0] = 1 - self.pop_param[:,4]
        self.pop_dyn[:,0,1] = self.pop_param[:,4]
        self.pop_dyn[:,0,4] = np.random.randint(0,100,self.n)
        self.pop_dyn[:,0,5] = np.random.randint(0,100,self.n)
        self.pop_dyn[:,0,6] = np.random.randint(0,100,self.n)
        self.pop_dyn[:,0,7] = np.random.randint(0,100,self.n)
        self.pop_dyn[:,:,8] = -np.ones((self.n,self.n_time))
        self.pop_dyn[:,:,10] = -np.ones((self.n,self.n_time))
        for i in self.get_infected(0):
            self.pop_dyn[i,0,8] = self.pop_param[i,0]

    def get_pos(self,t):
        return self.pop_dyn[:,t,4:6]

    def get_signal(self, t):
        # return all non protected having a contact in previous time with a Syp
        t_init = max(0,t-self.delta_time)
        mat_contact = np.sum(self.tensor_contact[:,:,t_init:t],axis=2)-self.delta_time*np.eye(self.n,self.n)
        symptoms = np.sum(self.pop_dyn[:,t_init:t,2],axis=1)*(1-self.pop_dyn[:,t_init,2])
        contact = mat_contact.dot(symptoms*(self.pop_param[:,5]))*(1-self.pop_dyn[:,t,9])*(self.pop_param[:,5])
        return [i for (i,c) in enumerate(contact) if c>0]

    def make_contact_matrix(self,t):
        vec_dist = spatial.distance.pdist(self.pop_dyn[:,t,4:6],'euclidean')
        return spatial.distance.squareform(vec_dist)<self.r_cont

    def make_dplt(self, t):
    # return the new position and the list of individuals arrived at destination
        vec_to_dest = (self.pop_dyn[:,t,6:8]-self.pop_dyn[:,t,4:6])
        dist_to_dest = np.sqrt(np.sum(vec_to_dest**2,1))
        fixed = self.get_fixed(t)
        frac = np.expand_dims((fixed*self.pop_param[:,3])/(dist_to_dest+0.00001),axis=1)
        mask = frac<1
        #print((mask*frac*vec_to_dest))
        self.pop_dyn[:,t+1,4:6] = mask*(self.pop_dyn[:,t,4:6]+frac*vec_to_dest)+(1-mask)*self.pop_dyn[:,t,6:8]
        return [i for (i,c) in enumerate(frac>1) if c]

    def make_new_dest(self, t, arrived):
        #print(arrived)
        self.pop_dyn[:,t,6:8] = self.pop_dyn[:,t-1,6:8]
        for i in arrived:
            self.pop_dyn[i,t,6:8] = np.random.randint(0,100,2)
            #print(i, self.pop_dyn[i,t,5:9])

    def make_step_mvt(self,t):
        arrived = self.make_dplt(t)
        self.make_new_dest(t+1, arrived)
        self.tensor_contact[:,:,t+1] = self.make_contact_matrix(t+1)
    
    def make_S2I(self,t):
        self.pop_dyn[:,t+1,0] = self.pop_dyn[:,t,0]
        infectious = self.pop_dyn[:,t,1]*(1-self.pop_dyn[:,t,9])
        possible_new_infection = (self.tensor_contact[:,:,t]-np.eye(self.n,self.n)).dot(infectious)*(self.pop_dyn[:,t,0])*(1-self.pop_dyn[:,t,9])
        for i,c in enumerate(possible_new_infection):
            if c>1 and np.random.random() < self.p_cont:
                #print(t, 'infection', i)
                self.pop_dyn[i,t+1,0:2] = [0,1]
                self.pop_dyn[i,t+1,8] = self.pop_param[i,0]

    def make_2P(self,t):
        for i in self.get_signal(t):
            self.pop_dyn[i,t+1,9] = 1
            if self.pop_dyn[i,t,10] < 0:
                self.pop_dyn[i,t+1,10] = self.time_protected     

    def get_infected(self, t):
        return [i for (i,c) in enumerate(self.pop_dyn[:,t,1]) if c]

    def get_susceptible(self, t):
        return [i for (i,c) in enumerate(self.pop_dyn[:,t,0]) if c]

    def get_symptom(self, t):
        return [i for (i,c) in enumerate(self.pop_dyn[:,t,2]) if c]

    def get_last(self, t):
        return [i for (i,c) in enumerate(self.pop_dyn[:,t,3]) if c]

    def get_fixed(self, t):
        # return 0 if fixed!
        return (1-(self.pop_dyn[:,t,2]+self.pop_dyn[:,t,9])>0)
    
    def get_protected(self,t):
        return [i for (i,c) in enumerate(self.pop_dyn[:,t,9]) if c]

    def check_I(self,t):
        # check for I(t) if transition to Sy(t+1)
        for i in self.get_infected(t):
            timer = self.pop_dyn[i,t,8]
            if timer > 1:
                #print(i,timer)
                self.pop_dyn[i,t+1,8] = timer -1
                self.pop_dyn[i,t+1,1] = 1
            else:
                #print(t, 'symptom', i)
                self.pop_dyn[i,t+1,1:3] = [0,1]
                self.pop_dyn[i,t+1,8] = self.pop_param[i,1]

    def make_test(self,t):
        indice_test = range(self.indices[t%self.n_indices][0], self.indices[t%self.n_indices][1])
        #print(indice_test)
        positive_test = set(indice_test).intersection(set(self.get_infected(t)))
        for i in positive_test:
            self.pop_dyn[i,t+1,9] = 1
            if self.pop_dyn[i,t,10] < 0:
                self.pop_dyn[i,t+1,10] = self.time_protected
    
    def check_P(self,t):
        # check for P(t) if transition to NotP(t+1)
        for i in self.get_protected(t):
            timer = self.pop_dyn[i,t,10]
            if timer > 1:
                self.pop_dyn[i,t+1,10] = timer -1
                self.pop_dyn[i,t+1,9] = 1
            else:
                self.pop_dyn[i,t+1,10] = -1
                self.pop_dyn[i,t+1,9] = 0
                #if i == 100:
                #    print(t,timer, self.pop_dyn[i,t:,9] )#np.zeros(self.n_time-t-1)
                  
    def check_Sy(self,t):
        # check for Sy(t) if transition L(t+1)
        for i in self.get_symptom(t):
            timer = self.pop_dyn[i,t,8]
            if timer > 1:
                self.pop_dyn[i,t+1,8] = timer -1
                self.pop_dyn[i,t+1,2] = 1
            else:
                self.pop_dyn[i,t+1,2:4] = [0,1]
                self.pop_dyn[i,t+1:,3] = np.ones(self.n_time-t-1)
                #print(i,'test', self.pop_dyn[i,t+1,0:4])

    def make_simu(self):
        for t in range(self.n_time-1):
            self.check_I(t)
            self.check_Sy(t)
            self.check_P(t)
            self.make_2P(t)
            self.make_S2I(t)
            self.make_step_mvt(t)

    def make_simu_test(self):
        for t in range(self.n_time-1):
            self.check_I(t)
            self.check_Sy(t)
            self.check_P(t)
            self.make_test(t)
            self.make_S2I(t)
            self.make_step_mvt(t)

            
    def all_infected(self):
        return np.sum(self.pop_dyn[:,:,1],axis=0)/self.n

    def all_susceptible(self):
        return np.sum(self.pop_dyn[:,:,0],axis=0)/self.n

    def all_symptoms(self):
        return np.sum(self.pop_dyn[:,:,2],axis=0)/self.n

    def all_last(self):
        return np.sum(self.pop_dyn[:,:,3],axis=0)/self.n

    def all_protected_infected(self):
        return np.sum(self.pop_dyn[:,:,9]*self.pop_dyn[:,:,1],axis=0)/self.n

    def all_protected_susceptible(self):
        return np.sum(self.pop_dyn[:,:,9]*self.pop_dyn[:,:,0],axis=0)/self.n

    def all_protected_symptoms(self):
        return np.sum(self.pop_dyn[:,:,9]*self.pop_dyn[:,:,2],axis=0)/self.n

    def all_protected_last(self):
        return np.sum(self.pop_dyn[:,:,9]*self.pop_dyn[:,:,3],axis=0)/self.n






    
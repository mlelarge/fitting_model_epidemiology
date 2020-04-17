import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def get_color(l):
    if l[0] and l[9]:
        # su and protected
        return 'green'
    elif l[0]:
        # su and not protected
        return 'blue'
    elif l[1] and l[9]:
        # infected and protected
        return 'orange'
    elif l[1]:
        # infected and not protected
        return 'red'
    elif l[2]:
        # symp
        return 'yellow'
    elif l[3]:
        # rec
        return 'grey'
    else:
        # just to check
        return 'black'

def make_anim(simu):
    infected = simu.all_infected()
    susceptible = simu.all_susceptible()
    symptoms = simu.all_symptoms()
    recovered = simu.all_last()
    fig = plt.figure(figsize=(14,7))
    ax = fig.add_subplot(1,2,1)
    cx = fig.add_subplot(1,2,2)
    ax.axis('off')
    cx.axis([0,simu.n_time,0,1])
    pos_init = simu.get_pos(0)
    scatt = ax.scatter(pos_init[:,0], pos_init[:,1], c='blue',s=8)
    case = plt.Rectangle((0,0),100,100,fill=False)
    ax.add_patch(case)
    cvst, = cx.plot(infected[0], color="red",label="Infected")
    rvst, = cx.plot(recovered[0], color="gray",label="Recovered")
    syst, = cx.plot(symptoms[0], color='yellow',label='Symptoms')
    sst, = cx.plot(susceptible[0], color='green',label='Susceptible')
    cx.legend(handles = [sst,cvst,syst,rvst])
    cx.set_xlabel("Time")
    cx.set_ylabel("Fraction population")

    def update(t):
        pos = simu.get_pos(t)
        offsets=np.array([pos[:,0],pos[:,1]])
        scatt.set_offsets(np.ndarray.transpose(offsets))
        colors = [get_color(p) for p in simu.pop_dyn[:,t]]
        scatt.set_color(colors)
        cvst.set_data(range(t),infected[:t])
        rvst.set_data(range(t),recovered[:t])
        syst.set_data(range(t),symptoms[:t])
        sst.set_data(range(t),susceptible[:t])
        return scatt, cvst, rvst, syst, sst
    return animation.FuncAnimation(fig, update, np.arange(1, simu.n_time), interval=50, blit=True)
    
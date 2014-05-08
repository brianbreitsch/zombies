import numpy as np
import matplotlib.pyplot as plt

xlim = (-0.1, 200.0)
ylim = (-0.1, 200.0)
tlim = (0., 1, 10000)
def f(Y, t):
    h, z = Y
    alpha = 1.0e-2
    beta = 0.2e-2
    #return [-h*h*z*alpha, h*h*z*alpha-z*h*beta]
    return [-h*h*z*alpha, h*h*z*alpha-z**1.8*(h**0.4+100)*beta]

y1 = np.linspace(0.0, 200.0, 40)
y2 = np.linspace(0.0, 200.0, 40)

Y1, Y2 = np.meshgrid(y1, y2)

t = 0

u, v = np.zeros(Y1.shape), np.zeros(Y2.shape)

NI, NJ = Y1.shape

for i in range(NI):
    for j in range(NJ):
        x = Y1[i, j]
        y = Y2[i, j]
        yprime = f([x, y], t)
        u[i,j] = yprime[0]
        v[i,j] = yprime[1]
     
fig = plt.figure()
ax = fig.add_subplot(111)
Q = ax.quiver(Y1, Y2, u, v, color='r')

plt.xlabel('humans')
plt.ylabel('zombies')
plt.xlim(xlim)
plt.ylim(ylim)
#plt.savefig('images/phase-portrait.png')

datafile = open('data', 'r')
populations = np.load(datafile)
end = np.where(populations[:,0]==0)[0][0]
print('end: {0}'.format(end))
z0 = populations[0,1]
h0 = populations[0,2]

from scipy.integrate import odeint

def onclick(event):
    if event.button==3:
        tspan = np.linspace(tlim[0], tlim[1], tlim[2])
        y0 = [event.xdata, event.ydata]
        ys = odeint(f, y0, tspan)
        e1 = np.argmax(ys[:,0] < xlim[0])
        e2 = np.argmax(ys[:,0] > xlim[1])
        e3 = np.argmax(ys[:,1] < ylim[0])
        e4 = np.argmax(ys[:,1] > ylim[1])
        m = max(e1,e2,e3,e4)
        e = -1
        if m != 0:
            e1 = e1 if e1 != 0 else m
            e2 = e2 if e2 != 0 else m
            e3 = e3 if e3 != 0 else m
            e4 = e4 if e4 != 0 else m
            e = min(e1,e2,e3,e4)

        ax.plot(ys[0:e,0], ys[0:e,1], 'b-') # path
        fig.canvas.draw()

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.xlim([xlim[0], xlim[1]])
   
plt.plot(populations[0:end,1], populations[0:end,2], 'o')

datafile.close()
plt.show()


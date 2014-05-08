import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

n_humans = 150
n_zombies = 50
field_size = .8e3
incubation_period = 6

def delx_dely(x1, y1, x2, y2):
    dx = x2 - x1
    #if dx > field_size / 2.:
    #    dx -= field_size
    #elif dx < -field_size / 2.:
    #    dx += field_size
    dy = y2 - y1
    #if dy > field_size / 2.:
    #    dy -= field_size
    #elif dy < -field_size / 2.:
    #    dy += field_size
    return dx, dy



class Human:

    v = 4.8
    sigma = 300.
    attack_radius = 30.
    attack_success = 0.1
    moment_weight = 5.
    near_weight = 7.
    noise_weight = 4.

    def __init__(self, x = 0., y = 0.):
        self.x = x
        self.y = y
        self.infected = False
        self.infection_time = 0

    def act(self):
        hx, hy = self.x, self.y
        mx, my = 0., 0.
        nearest = field_size / 2.
        near_x, near_y = 0., 0.
        for zombie in zombies:
            zx, zy = zombie.x, zombie.y
            dx, dy = delx_dely(hx, hy, zx, zy)
            hz_norm = np.sqrt(dx**2 + dy**2)
            # check if nearest zombie
            if hz_norm < nearest:
                nearest = hz_norm
                near_x, near_y = dx / hz_norm, dy / hz_norm
            # attempt attack if possible
            if hz_norm < Human.attack_radius:
                if np.random.random() < Human.attack_success:
                    zombie.hp -= 1
            if hz_norm > 0:
                mx += dx / hz_norm * np.exp( -( dx / Human.sigma) ** 2)
                my += dy / hz_norm * np.exp( -( dy / Human.sigma) ** 2)
        m_norm = np.sqrt(mx**2 + my**2)
        mx = mx / m_norm if m_norm != 0 else 0
        my = my / m_norm if m_norm != 0 else 0
        # add moment, nearest, random effects to motion
        newx = Human.moment_weight * mx + Human.near_weight * near_x + Human.noise_weight * np.random.randn()
        newy = Human.moment_weight * my + Human.near_weight * near_y + Human.noise_weight * np.random.randn()
        new_norm = np.sqrt(newx**2 + newy**2)
        newx = hx - newx / new_norm * Human.v
        newy = hy - newy / new_norm * Human.v
        # field wrap
        if newx < 0:
            self.x = 0.
        elif newx > field_size:
            self.x = field_size
        else:
            self.x = newx
        if newy < 0:
            self.y = 0.
        elif newy > field_size:
            self.y = field_size
        else:
            self.y = newy


class Zombie:

    v = 5.
    sigma = 120.
    attack_radius = 20.
    attack_success = .95
    moment_weight = 8.
    near_weight = 10.
    noise_weight = 2.

    def __init__(self, x = 0., y = 0.):
        self.x = x
        self.y = y
        self.hp = 10

    def act(self):
        zx, zy = self.x, self.y
        mx, my = 0., 0.
        nearest = field_size / 2.
        near_x, near_y = 0., 0.
        for human in humans:
            hx, hy = human.x, human.y
            dx, dy = delx_dely(hx, hy, zx, zy)
            hz_norm = np.sqrt(dx**2 + dy**2)
            # check if nearest zombie
            if hz_norm < nearest:
                nearest = hz_norm
                near_x, near_y = dx / hz_norm, dy / hz_norm
            # attempt attack if possible
            if hz_norm < Zombie.attack_radius:
                if np.random.random() < Zombie.attack_success:
                    human.infected = True
            if hz_norm > 0:
                mx += dx / hz_norm * np.exp( -( hz_norm / Zombie.sigma) ** 2)
                my += dy / hz_norm * np.exp( -( hz_norm / Zombie.sigma) ** 2)
        m_norm = np.sqrt(mx**2 + my**2)
        mx = mx / m_norm if m_norm != 0 else 0
        my = my / m_norm if m_norm != 0 else 0
        # apply moment, random components to motion
        newx = Zombie.moment_weight * mx + Zombie.near_weight * near_x + Zombie.noise_weight * np.random.randn()
        newy = Zombie.moment_weight * my + Zombie.near_weight * near_y + Zombie.noise_weight * np.random.randn()
        new_norm = np.sqrt(newx**2 + newy**2)
        newx = zx - newx / new_norm * Zombie.v
        newy = zy - newy / new_norm * Zombie.v
        # field wrap
        if newx < 0:
            self.x = 0.
        elif newx > field_size:
            self.x = field_size
        else:
            self.x = newx
        if newy < 0:
            self.y = 0.
        elif newy > field_size:
            self.y = field_size
        else:
            self.y = newy


def carnage():
    for zombie in zombies:
        if zombie.hp <= 0:
            zombies.remove(zombie)
    for human in humans:
        if human.infected:
            human.infection_time += 1
            if human.infection_time >= incubation_period:
                zombies.append(Zombie(human.x, human.y))
                humans.remove(human)


# populate human array
humans = [Human(np.random.random() * field_size, np.random.random() * field_size) for i in range(n_humans)] 

# populate zombie array
zombies = [Zombie(np.random.random() * field_size, np.random.random() * field_size) for i in range(n_zombies)] 


def step():
    for zombie in zombies:
        zombie.act()
    for human in humans:
        human.act()
    carnage()

fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-10, field_size+10), ylim=(-10, field_size+10))
humans_plt, = ax.plot([], [], 'bo', ms=4.)
zombies_plt, = ax.plot([], [], 'go', ms=6.)

def init_anim():
    humans_plt.set_data([], [])
    zombies_plt.set_data([], [])
    return [],

def animate(i):
    step()
    humans_plt.set_data([h.x for h in humans], [h.y for h in humans])
    zombies_plt.set_data([z.x for z in zombies], [z.y for z in zombies])
    return humans_plt, zombies_plt,

ani = animation.FuncAnimation(fig, animate, frames=1, interval=90, blit=False, init_func=init_anim)
plt.show()


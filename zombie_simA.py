import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Human:

    v = 5.
    sigma = 300.
    attack_radius = 40.
    attack_success = 0.07
    moment_weight = 0.
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
            self.x = newx + field_size
        elif newx > field_size:
            self.x = newx - field_size
        else:
            self.x = newx
        if newy < 0:
            self.y = newy + field_size
        elif newy > field_size:
            self.y = newy - field_size
        else:
            self.y = newy


class Zombie:

    v = 5.5
    sigma = 75.
    attack_radius = 10.
    attack_success = .9
    moment_weight = 8.
    near_weight = 10.
    noise_weight = 4.

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
            self.x = newx + field_size
        elif newx > field_size:
            self.x = newx - field_size
        else:
            self.x = newx
        if newy < 0:
            self.y = newy + field_size
        elif newy > field_size:
            self.y = newy - field_size
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


def delx_dely(x1, y1, x2, y2):
    dx = x2 - x1
    if dx > field_size / 2.:
        dx -= field_size
    elif dx < -field_size / 2.:
        dx += field_size
    dy = y2 - y1
    if dy > field_size / 2.:
        dy -= field_size
    elif dy < -field_size / 2.:
        dy += field_size
    return dx, dy


n_humans = 150
n_zombies = 10
n_steps = 6000
field_size = .8e3
incubation_period = 10

# populate human array
humans = [Human(np.random.random() * field_size, np.random.random() * field_size) for i in range(n_humans)] 

# populate zombie array
zombies = [Zombie(np.random.random() * field_size, np.random.random() * field_size) for i in range(n_zombies)] 

pop_array_len = n_zombies + n_humans * 2
populations = np.zeros((pop_array_len, 3))
pop_array_ind = 0

i = 0
while n_zombies > 0 and n_humans > 0:
    for zombie in zombies:
        zombie.act()
    for human in humans:
        human.act()
    carnage()
    if n_humans != len(humans) or n_zombies != len(zombies):
        n_humans = len(humans)
        n_zombies = len(zombies)
        populations[pop_array_ind, :] = i, n_humans, n_zombies
        pop_array_ind += 1
    i += 1
    if i > n_steps:
        break
    print('{0}\t{1}\t{2}'.format(i,n_humans, n_zombies))

f = open('data', 'w')                                                           
np.save(f, populations)                                                         
f.close()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(populations[0:pop_array_ind,0], populations[0:pop_array_ind,1])
ax.plot(populations[0:pop_array_ind,0], populations[0:pop_array_ind,2])

plt.show()

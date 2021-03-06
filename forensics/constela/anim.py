from matplotlib import pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation


fig = plt.figure()
ax = p3.Axes3D(fig)

dat = [( 0, 0), ( 0, 1), ( 0, 2), ( 0, 3), ( 0, 4), ( 0, 5), ( 0, 6), ( 0, 10), ( 0, 11), ( 0, 15), ( 0, 18), ( 0, 19), ( 0, 20), ( 0, 21), ( 0, 22), ( 0, 23), ( 0, 24), ( 1, 0), ( 1, 6), ( 1, 9), ( 1, 10), ( 1, 12), ( 1, 13), ( 1, 14), ( 1, 16), ( 1, 18), ( 1, 24), ( 2, 0), ( 2, 2), ( 2, 3), ( 2, 4), ( 2, 6), ( 2, 9), ( 2, 12), ( 2, 14), ( 2, 15), ( 2, 18), ( 2, 20), ( 2, 21), ( 2, 22), ( 2, 24), ( 3, 0), ( 3, 2), ( 3, 3), ( 3, 4), ( 3, 6), ( 3, 8), ( 3, 9), ( 3, 15), ( 3, 18), ( 3, 20), ( 3, 21), ( 3, 22), ( 3, 24), ( 4, 0), ( 4, 2), ( 4, 3), ( 4, 4), ( 4, 6), ( 4, 8), ( 4, 10), ( 4, 11), ( 4, 12), ( 4, 16), ( 4, 18), ( 4, 20), ( 4, 21), ( 4, 22), ( 4, 24), ( 5, 0), ( 5, 6), ( 5, 10), ( 5, 13), ( 5, 18), ( 5, 24), ( 6, 0), ( 6, 1), ( 6, 2), ( 6, 3), ( 6, 4), ( 6, 5), ( 6, 6), ( 6, 8), ( 6, 10), ( 6, 12), ( 6, 14), ( 6, 16), ( 6, 18), ( 6, 19), ( 6, 20), ( 6, 21), ( 6, 22), ( 6, 23), ( 6, 24), ( 7, 10), ( 7, 12), ( 7, 14), ( 7, 16), ( 8, 0), ( 8, 1), ( 8, 5), ( 8, 6), ( 8, 7), ( 8, 9), ( 8, 13), ( 8, 15), ( 8, 16), ( 8, 20), ( 8, 21), ( 9, 0), ( 9, 2), ( 9, 3), ( 9, 7), ( 9, 8), ( 9, 9), ( 9, 10), ( 9, 11), ( 9, 12), ( 9, 17), ( 9, 20), ( 9, 22), ( 10, 0), ( 10, 1), ( 10, 2), ( 10, 3), ( 10, 4), ( 10, 6), ( 10, 7), ( 10, 8), ( 10, 10), ( 10, 12), ( 10, 15), ( 10, 17), ( 10, 18), ( 10, 19), ( 10, 20), ( 10, 23), ( 10, 24), ( 11, 2), ( 11, 8), ( 11, 9), ( 11, 15), ( 11, 16), ( 11, 17), ( 11, 18), ( 11, 19), ( 11, 20), ( 11, 21), ( 11, 24), ( 12, 0), ( 12, 4), ( 12, 5), ( 12, 6), ( 12, 9), ( 12, 11), ( 12, 15), ( 12, 16), ( 12, 18), ( 12, 20), ( 12, 21), ( 13, 0), ( 13, 4), ( 13, 5), ( 13, 9), ( 13, 11), ( 13, 13), ( 13, 15), ( 13, 16), ( 13, 19), ( 13, 21), ( 14, 0), ( 14, 2), ( 14, 3), ( 14, 4), ( 14, 5), ( 14, 6), ( 14, 8), ( 14, 9), ( 14, 13), ( 14, 14), ( 14, 15), ( 14, 16), ( 14, 18), ( 14, 19), ( 14, 20), ( 14, 22), ( 14, 23), ( 14, 24), ( 15, 0), ( 15, 2), ( 15, 3), ( 15, 8), ( 15, 9), ( 15, 10), ( 15, 12), ( 15, 14), ( 15, 16), ( 15, 17), ( 15, 20), ( 15, 21), ( 15, 22), ( 16, 0), ( 16, 3), ( 16, 4), ( 16, 5), ( 16, 6), ( 16, 7), ( 16, 10), ( 16, 12), ( 16, 13), ( 16, 15), ( 16, 16), ( 16, 17), ( 16, 18), ( 16, 19), ( 16, 20), ( 16, 22), ( 16, 23), ( 16, 24), ( 17, 8), ( 17, 10), ( 17, 11), ( 17, 14), ( 17, 15), ( 17, 16), ( 17, 20), ( 17, 22), ( 18, 0), ( 18, 1), ( 18, 2), ( 18, 3), ( 18, 4), ( 18, 5), ( 18, 6), ( 18, 8), ( 18, 9), ( 18, 10), ( 18, 11), ( 18, 12), ( 18, 14), ( 18, 16), ( 18, 18), ( 18, 20), ( 18, 24), ( 19, 0), ( 19, 6), ( 19, 8), ( 19, 9), ( 19, 10), ( 19, 14), ( 19, 16), ( 19, 20), ( 19, 21), ( 19, 23), ( 20, 0), ( 20, 2), ( 20, 3), ( 20, 4), ( 20, 6), ( 20, 9), ( 20, 11), ( 20, 12), ( 20, 13), ( 20, 14), ( 20, 15), ( 20, 16), ( 20, 17), ( 20, 18), ( 20, 19), ( 20, 20), ( 20, 22), ( 20, 23), ( 21, 0), ( 21, 2), ( 21, 3), ( 21, 4), ( 21, 6), ( 21, 9), ( 21, 10), ( 21, 15), ( 21, 17), ( 21, 18), ( 21, 19), ( 21, 21), ( 21, 22), ( 21, 23), ( 21, 24), ( 22, 0), ( 22, 2), ( 22, 3), ( 22, 4), ( 22, 6), ( 22, 9), ( 22, 14), ( 22, 21), ( 22, 24), ( 23, 0), ( 23, 6), ( 23, 8), ( 23, 10), ( 23, 15), ( 23, 16), ( 23, 21), ( 23, 24), ( 24, 0), ( 24, 1), ( 24, 2), ( 24, 3), ( 24, 4), ( 24, 5), ( 24, 6), ( 24, 8), ( 24, 11), ( 24, 12), ( 24, 16), ( 24, 17), ( 24, 18), ( 24, 19), ( 24, 21), ( 24, 22), ( 24, 24) ]

import numpy as np
omg = 5.0
M = len(dat)
# Creating dataset
z = [x[0] for x in dat]
x = [x[1] for x in dat]
y = np.random.randint(-10,10, size =(M))
y = [float(v) for v in y]

points, = ax.plot(x, y, z, 's',markersize=8)
txt = fig.suptitle('')


t = 0.0
dt = 0.01

def update_points(num, x, y, z, points):
    global t
    t += dt
    txt.set_text('OSIRIS CONSTELLATION')
    new_x = x
    new_y = np.zeros(M,dtype=float)
    for i in range(M):
        new_y[i] = y[i]*np.cos(omg*t)
    new_z = z
    # update properties
    points.set_data(new_x,new_y)
    points.set_3d_properties(new_z, 'z')
    

    # return modified artists
    return points,txt

ani=animation.FuncAnimation(fig, update_points, frames=20, fargs=(x, y, z, points))

plt.show()
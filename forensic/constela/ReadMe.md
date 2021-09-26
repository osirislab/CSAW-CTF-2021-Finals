## OSIRIS Constellation
We have a bunch of packets, from Xi -> Yi, with timestaps, each showing the destination between Xi, Yi (and each of these ip's correspond to a satelite in this constellation). And we have so many of these over a long time, so we can for say time t : t+dt have an estimate of where each satelite is if we parse through the PCAPs, order them through time, and solve a system of equations (with say, scipy or some generic guess, and make it better gradually, or even optimization libs) to get the coordinates of satelites. </br>

We then plot these coordinates, over time, to see an animation. To see the animation, run "poc.py". Can you get the flag?

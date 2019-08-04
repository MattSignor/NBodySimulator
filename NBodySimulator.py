from numpy import *
from vpython import *


# This project was created to simulate N-Body Orbits.


class NBody:
    # This Object will be the entire system of n bodies where the position mass velocity radius and acc are all
    # created as numpy arrays.

    def __init__(self, pos, mass, velocity, radius, acc):

        self.pos = pos
        self.velocity = velocity
        self.mass = mass
        self.radius = radius
        self.acc = acc

    # This method is created to update the position array using the velocity array and the time step

    def updatepos(self, timestep, n):
        a = self.pos
        b = self.velocity

        for i in range(0, n):

            for j in range(0, 3):  # 0, 1 ,2 for 3 dimentions

                a[i][j] = a[i][j] + b[i][j] * timestep / 2
        return a

    # This method updates the velocity array

    def updatevel(self, timestep, n):
        a = self.velocity
        b = self.acc

        for i in range(0, n):

            for j in range(0, 3):  # dimentions

                a[i][j] = a[i][j] + (b[i][j] * timestep)

    # The array's below is a work around solution to a very strange problem. For some reason elements of certain
    # numpy arrays are not assigning their values to another numpy array. This fixed the problem, but it would be
    # interesting to farther investigate this issue.

    c = array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])  # work around for 4 body
    d = array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    e = array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]])

    # calculates the acceleration between n bodies
    def acceleration(self, n):

        a = self.pos
        accell = self.acc
        m = self.mass
        G = 6.67408e-11

        for i in range(0, n):
            # This is another consequence of the problem before
            for j in range(0, 3):
                if n == 4:
                    c[i][j] = 0
                elif n == 3:
                    d[i][j] = 0
                elif n == 5:
                    e[i][j] = 0

        for i in range(0, n):

            for j in range(0, n):

                if j != i:

                    for k in range(0, 3):
                        # Final consequence of problem
                        if n == 4:  # Four Body Case

                            c[i][k] = accell[i][k] - (G * m[j] * (a[i][k] - a[j][k])) / (
                                        self.dist(i, j) * self.dist(i, j) * self.dist(i, j))

                            accell = c
                            self.acc = accell

                        elif n == 3:  # Three Body Case

                            d[i][k] = accell[i][k] - (1.0 * m[j] * (a[i][k] - a[j][k])) / (
                                    self.dist(i, j) * self.dist(i, j) * self.dist(i, j))  # Use G = 1 for Figure 8

                            self.acc = d

                        elif n == 5:  # Five Body Case
                            e[i][k] = accell[i][k] - (G * m[j] * (a[i][k] - a[j][k])) / (
                                    self.dist(i, j) * self.dist(i, j) * self.dist(i, j))

                            self.acc = e

        return accell

    # calculates Euclidean Distance between points in arrays
    def dist(self, d, e):

        return linalg.norm(self.pos[d] - self.pos[e])

    # Extract numbers from array and vpython vector it
    def vextract(self, array, row):
        return vector(array[row][0], array[row][1], array[row][2])


if __name__ == "__main__":
    # In the main code we have an input statement that will allow the user to pick which animation they want to run
    # The current available animations triggers are: 3,4,4B,5

    q = input("Enter number of bodies example: ")
    if q == "4":
        # initialize vpython
        scene.forward = vector(0, -1, -10)

        # We need to make an n body system with position, velocity and mass arrays
        # This four-body system uses actual data of our solarsystem: Sun, Mercury, Venus and Earth
        fourbodysystem = NBody(array([[0, 0, 0], [0, 5.7e10, 0], [0, 1.1e11, 0], [0, 1.5e11, 0]], dtype=float),
                               array([2e30, 3.285e23, 4.8e24, 2.4e24]),
                               array([[0, 0, 0], [4.7e4, 0, 0], [3.5e4, 0, 0], [30000, 0, 0]], dtype=float),
                               array([695510, 2439.7, 6051.8, 6378.1], dtype=float),
                               array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=float))

        c = array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=float)  # initialize four body acceleration array
        # One of the factors that influences the speed of the animation and the accuraccy of the integration
        timestep = 1000

        sun1 = sphere(pos=fourbodysystem.vextract(fourbodysystem.pos, 0), radius=fourbodysystem.radius[0] * 10000,
                      color=color.yellow, retain=1000000, interval=10, make_trail=True)
        sun1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 0)
        mercury1 = sphere(pos=fourbodysystem.vextract(fourbodysystem.pos, 1), radius=fourbodysystem.radius[1] * 1000000,
                          color=color.red, retain=1000000, interval=10, make_trail=True)
        mercury1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 1)

        venus1 = sphere(pos=fourbodysystem.vextract(fourbodysystem.pos, 2), radius=fourbodysystem.radius[2] * 1000000,
                        color=color.orange, retain=1000000000, interval=10, make_trail=True)
        venus1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 2)

        earth1 = sphere(pos=fourbodysystem.vextract(fourbodysystem.pos, 3), radius=fourbodysystem.radius[3] * 1000000,
                        color=color.blue, retain=1000000000, interval=10, make_trail=True)
        earth1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 3)

        while True:
            # rate(1000000)
            fourbodysystem.updatepos(timestep, 4)
            sun1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 0)
            sun1.pos = fourbodysystem.vextract(fourbodysystem.pos, 0)
            mercury1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 1)
            mercury1.pos = fourbodysystem.vextract(fourbodysystem.pos, 1)
            venus1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 2)
            venus1.pos = fourbodysystem.vextract(fourbodysystem.pos, 2)
            earth1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 3)
            earth1.pos = fourbodysystem.vextract(fourbodysystem.pos, 3)

            # print("pos2",fourbodysystem.updatepos(timestep,4))
            fourbodysystem.acceleration(4)
            sun1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 0)
            sun1.pos = fourbodysystem.vextract(fourbodysystem.pos, 0)
            mercury1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 1)
            mercury1.pos = fourbodysystem.vextract(fourbodysystem.pos, 1)
            venus1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 2)
            venus1.pos = fourbodysystem.vextract(fourbodysystem.pos, 2)
            earth1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 3)
            earth1.pos = fourbodysystem.vextract(fourbodysystem.pos, 3)

            # print("acc",fourbodysystem.acceleration(4))
            fourbodysystem.updatevel(timestep, 4)
            sun1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 0)
            sun1.pos = fourbodysystem.vextract(fourbodysystem.pos, 0)
            mercury1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 1)
            mercury1.pos = fourbodysystem.vextract(fourbodysystem.pos, 1)
            venus1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 2)
            venus1.pos = fourbodysystem.vextract(fourbodysystem.pos, 2)
            earth1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 3)
            earth1.pos = fourbodysystem.vextract(fourbodysystem.pos, 3)

            # print("vel",fourbodysystem.updatevel(timestep,4))
            fourbodysystem.updatepos(timestep, 4)
            sun1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 0)
            sun1.pos = fourbodysystem.vextract(fourbodysystem.pos, 0)
            mercury1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 1)
            mercury1.pos = fourbodysystem.vextract(fourbodysystem.pos, 1)
            venus1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 2)
            venus1.pos = fourbodysystem.vextract(fourbodysystem.pos, 2)
            earth1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 3)
            earth1.pos = fourbodysystem.vextract(fourbodysystem.pos, 3)

            # print("pos",fourbodysystem.pos)



    elif q == "4B":
        # initialize vpython
        scene.forward = vector(0, -1, -10)

        # We need to make an n body system with position, velocity and mass arrays
        fourbodysystem = NBody(array([[0, 0, 0], [0, 5.7e10, 0], [0, 1.1e11, 0], [0, 1.5e11, 0]], dtype=float),
                               array([2e30, 3.285e29, 4.8e30, 2.4e29]),
                               array([[1e4, 0, 5e4], [4.7e4, 0, 5e4], [3.5e4, 0, 0.5e4], [-3e4, 0, 5e4]], dtype=float),
                               array([695510, 2439.7, 6051.8, 6378.1], dtype=float),
                               array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=float))

        c = array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=float)  # initialize four body acceleration array
        timestep = 500

        sun1 = sphere(pos=fourbodysystem.vextract(fourbodysystem.pos, 0), radius=fourbodysystem.radius[0] * 10000,
                      color=color.yellow, retain=1000000, interval=10, make_trail=True)
        sun1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 0)
        mercury1 = sphere(pos=fourbodysystem.vextract(fourbodysystem.pos, 1), radius=fourbodysystem.radius[1] * 1000000,
                          color=color.red, retain=1000000, interval=10, make_trail=True)
        mercury1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 1)

        venus1 = sphere(pos=fourbodysystem.vextract(fourbodysystem.pos, 2), radius=fourbodysystem.radius[2] * 1000000,
                        color=color.orange, retain=1000000000, interval=10, make_trail=True)
        venus1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 2)

        earth1 = sphere(pos=fourbodysystem.vextract(fourbodysystem.pos, 3), radius=fourbodysystem.radius[3] * 1000000,
                        color=color.blue, retain=1000000000, interval=10, make_trail=True)
        earth1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 3)

        while True:
            rate(100000)
            fourbodysystem.updatepos(timestep, 4)
            sun1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 0)
            sun1.pos = fourbodysystem.vextract(fourbodysystem.pos, 0)
            mercury1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 1)
            mercury1.pos = fourbodysystem.vextract(fourbodysystem.pos, 1)
            venus1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 2)
            venus1.pos = fourbodysystem.vextract(fourbodysystem.pos, 2)
            earth1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 3)
            earth1.pos = fourbodysystem.vextract(fourbodysystem.pos, 3)

            # print("pos2",fourbodysystem.updatepos(timestep,4))
            fourbodysystem.acceleration(4)
            sun1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 0)
            sun1.pos = fourbodysystem.vextract(fourbodysystem.pos, 0)
            mercury1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 1)
            mercury1.pos = fourbodysystem.vextract(fourbodysystem.pos, 1)
            venus1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 2)
            venus1.pos = fourbodysystem.vextract(fourbodysystem.pos, 2)
            earth1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 3)
            earth1.pos = fourbodysystem.vextract(fourbodysystem.pos, 3)

            # print("acc",fourbodysystem.acceleration(4))
            fourbodysystem.updatevel(timestep, 4)
            sun1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 0)
            sun1.pos = fourbodysystem.vextract(fourbodysystem.pos, 0)
            mercury1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 1)
            mercury1.pos = fourbodysystem.vextract(fourbodysystem.pos, 1)
            venus1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 2)
            venus1.pos = fourbodysystem.vextract(fourbodysystem.pos, 2)
            earth1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 3)
            earth1.pos = fourbodysystem.vextract(fourbodysystem.pos, 3)

            # print("vel",fourbodysystem.updatevel(timestep,4))
            fourbodysystem.updatepos(timestep, 4)
            sun1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 0)
            sun1.pos = fourbodysystem.vextract(fourbodysystem.pos, 0)
            mercury1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 1)
            mercury1.pos = fourbodysystem.vextract(fourbodysystem.pos, 1)
            venus1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 2)
            venus1.pos = fourbodysystem.vextract(fourbodysystem.pos, 2)
            earth1.velocity = fourbodysystem.vextract(fourbodysystem.velocity, 3)
            earth1.pos = fourbodysystem.vextract(fourbodysystem.pos, 3)

            # print("pos",fourbodysystem.pos)

    elif q == "3":

        # Everything is normalized, such that a unique solution of the "Figure 8" can be demonstrated.
        # G = M1 = M2 = M3 = 1
        # The following inital conditions were found online in order to produce this solution

        # If switched to regular G, M = 1e29, same positions but e10 and velocities e4, timestep=100, you get chaos.

        timestep = 0.001
        d = array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=float)

        # initialize vpython
        scene.forward = vector(0, -1, -10)

        # We need to make an n body system with position, velocity and mass arrays
        threebodysystem = NBody(
            array([[0.97000436, -0.24308753, 0.4], [-0.97000436, 0.24308753, 0], [0, 0, 0.2]], dtype=float),
            array([1, 1, 1]),
            array([[0.466203685, 0.43236573, 0.2], [0.466203685, 0.43236573, 0.2], [-0.93240737, -0.86473146, 0.2]],
                  dtype=float),
            array([0.05, 0.05, 0.05], dtype=float),
            array([[0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=float))

        p1 = sphere(pos=threebodysystem.vextract(threebodysystem.pos, 0), radius=threebodysystem.radius[0],
                    color=color.yellow, retain=1000000, interval=10, make_trail=True)
        p1.velocity = threebodysystem.vextract(threebodysystem.velocity, 0)
        p2 = sphere(pos=threebodysystem.vextract(threebodysystem.pos, 1), radius=threebodysystem.radius[1],
                    color=color.red, retain=1000000, interval=10, make_trail=True)
        p2.velocity = threebodysystem.vextract(threebodysystem.velocity, 1)

        p3 = sphere(pos=threebodysystem.vextract(threebodysystem.pos, 2), radius=threebodysystem.radius[2],
                    color=color.orange, retain=1000000000, interval=10, make_trail=True)
        p3.velocity = threebodysystem.vextract(threebodysystem.velocity, 2)

        while True:
            # Notice that we can run this code at a much smaller rate than before as the computer is dealing
            # with much smaller and more reasonable numbers.
            rate(100)
            threebodysystem.updatepos(timestep, 3)
            p1.velocity = threebodysystem.vextract(threebodysystem.velocity, 0)
            p1.pos = threebodysystem.vextract(threebodysystem.pos, 0)
            p2.velocity = threebodysystem.vextract(threebodysystem.velocity, 1)
            p2.pos = threebodysystem.vextract(threebodysystem.pos, 1)
            p3.velocity = threebodysystem.vextract(threebodysystem.velocity, 2)
            p3.pos = threebodysystem.vextract(threebodysystem.pos, 2)

            # print("pos2",threebodysystem.updatepos(timestep,4))
            threebodysystem.acceleration(3)
            p1.velocity = threebodysystem.vextract(threebodysystem.velocity, 0)
            p1.pos = threebodysystem.vextract(threebodysystem.pos, 0)
            p2.velocity = threebodysystem.vextract(threebodysystem.velocity, 1)
            p2.pos = threebodysystem.vextract(threebodysystem.pos, 1)
            p3.velocity = threebodysystem.vextract(threebodysystem.velocity, 2)
            p3.pos = threebodysystem.vextract(threebodysystem.pos, 2)

            # print("acc",threebodysystem.acceleration(4))
            threebodysystem.updatevel(timestep, 3)
            p1.velocity = threebodysystem.vextract(threebodysystem.velocity, 0)
            p1.pos = threebodysystem.vextract(threebodysystem.pos, 0)
            p2.velocity = threebodysystem.vextract(threebodysystem.velocity, 1)
            p2.pos = threebodysystem.vextract(threebodysystem.pos, 1)
            p3.velocity = threebodysystem.vextract(threebodysystem.velocity, 2)
            p3.pos = threebodysystem.vextract(threebodysystem.pos, 2)

            # print("vel",threebodysystem.updatevel(timestep,4))
            threebodysystem.updatepos(timestep, 3)
            p1.velocity = threebodysystem.vextract(threebodysystem.velocity, 0)
            p1.pos = threebodysystem.vextract(threebodysystem.pos, 0)
            p2.velocity = threebodysystem.vextract(threebodysystem.velocity, 1)
            p2.pos = threebodysystem.vextract(threebodysystem.pos, 1)
            p3.velocity = threebodysystem.vextract(threebodysystem.velocity, 2)
            p3.pos = threebodysystem.vextract(threebodysystem.pos, 2)

            # print("pos",threebodysystem.pos)


    elif q == "5":


        timestep = 1000
        e = array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=float)
        # initialize vpython
        scene.forward = vector(0, -1, -10)

        # We need to make an n body system with position, velocity and mass arrays
        fivebodysystem = NBody(
            array([[2e11, 0, 0], [0, 1e11, 0], [0, -1e11, 0], [-1e11, 0, 0], [1e11, 0, 0]], dtype=float),
            array([5e30, 5e30, 5e30, 5e30, 5e30]),
            array([[0, 2e4, 1e4], [4e4, 0, 0], [4e4, 0, 0], [0, 0, 0], [4e4, 0, 0]], dtype=float),
            array([3000, 3000, 3000, 3000, 3000], dtype=float),
            array([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=float))

        p1 = sphere(pos=fivebodysystem.vextract(fivebodysystem.pos, 0), radius=fivebodysystem.radius[0] * 1000000,
                    color=color.yellow, retain=1000000, interval=10, make_trail=True)
        p1.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 0)
        p2 = sphere(pos=fivebodysystem.vextract(fivebodysystem.pos, 1), radius=fivebodysystem.radius[1] * 1000000,
                    color=color.red, retain=1000000, interval=10, make_trail=True)
        p2.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 1)

        p3 = sphere(pos=fivebodysystem.vextract(fivebodysystem.pos, 2), radius=fivebodysystem.radius[2] * 1000000,
                    color=color.orange, retain=1000000000, interval=10, make_trail=True)
        p3.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 2)

        p4 = sphere(pos=fivebodysystem.vextract(fivebodysystem.pos, 3), radius=fivebodysystem.radius[3] * 1000000,
                    color=color.blue, retain=1000000000, interval=10, make_trail=True)
        p4.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 3)

        p5 = sphere(pos=fivebodysystem.vextract(fivebodysystem.pos, 4), radius=fivebodysystem.radius[3] * 1000000,
                    color=color.green, retain=1000000000, interval=10, make_trail=True)
        p5.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 4)

        while True:
            rate(1000)
            fivebodysystem.updatepos(timestep, 5)
            p1.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 0)
            p1.pos = fivebodysystem.vextract(fivebodysystem.pos, 0)
            p2.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 1)
            p2.pos = fivebodysystem.vextract(fivebodysystem.pos, 1)
            p3.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 2)
            p3.pos = fivebodysystem.vextract(fivebodysystem.pos, 2)
            p4.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 3)
            p4.pos = fivebodysystem.vextract(fivebodysystem.pos, 3)
            p5.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 4)
            p5.pos = fivebodysystem.vextract(fivebodysystem.pos, 4)

            # print("pos2",fivebodysystem.updatepos(timestep,4))
            fivebodysystem.acceleration(5)
            p1.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 0)
            p1.pos = fivebodysystem.vextract(fivebodysystem.pos, 0)
            p2.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 1)
            p2.pos = fivebodysystem.vextract(fivebodysystem.pos, 1)
            p3.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 2)
            p3.pos = fivebodysystem.vextract(fivebodysystem.pos, 2)
            p4.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 3)
            p4.pos = fivebodysystem.vextract(fivebodysystem.pos, 3)
            p5.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 4)
            p5.pos = fivebodysystem.vextract(fivebodysystem.pos, 4)

            # print("acc",fivebodysystem.acceleration(4))
            fivebodysystem.updatevel(timestep, 5)
            p1.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 0)
            p1.pos = fivebodysystem.vextract(fivebodysystem.pos, 0)
            p2.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 1)
            p2.pos = fivebodysystem.vextract(fivebodysystem.pos, 1)
            p3.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 2)
            p3.pos = fivebodysystem.vextract(fivebodysystem.pos, 2)
            p4.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 3)
            p4.pos = fivebodysystem.vextract(fivebodysystem.pos, 3)
            p5.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 4)
            p5.pos = fivebodysystem.vextract(fivebodysystem.pos, 4)

            # print("vel",fivebodysystem.updatevel(timestep,4))
            fivebodysystem.updatepos(timestep, 5)
            p1.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 0)
            p1.pos = fivebodysystem.vextract(fivebodysystem.pos, 0)
            p2.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 1)
            p2.pos = fivebodysystem.vextract(fivebodysystem.pos, 1)
            p3.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 2)
            p3.pos = fivebodysystem.vextract(fivebodysystem.pos, 2)
            p4.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 3)
            p4.pos = fivebodysystem.vextract(fivebodysystem.pos, 3)
            p5.velocity = fivebodysystem.vextract(fivebodysystem.velocity, 4)
            p5.pos = fivebodysystem.vextract(fivebodysystem.pos, 4)

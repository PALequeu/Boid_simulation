from p5 import setup, draw, size, background, run, color, Vector
import numpy as np
from boid import Boid


width = 1000
height = 1000

flock = [Boid(*np.random.rand(2)*1000, width, height) for _ in range(30)]


def setup():
    #this happens just once
    size(width, height) #instead of create_canvas


def draw():
    global flock
    count = 0
    leadi= 0
    background(30, 30, 47)

    for boid in flock:
        count+=1
        leadi+=1
        if (leadi == 1):
            boid.edges()
            boid.Leader("carré")
            boid.update("carré")
            boid.leadershow()

        else:
            boid.edges()
            boid.apply_behaviour(flock)
            boid.update("boids")
            boid.show(count,flock)

#run(frame_rate=100)
#run(frame_rate=200)
run()
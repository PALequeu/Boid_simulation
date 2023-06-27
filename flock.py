from p5 import Vector
import numpy as np
import pygame
from boid import Boid


class Flock() :
    
    def __init__(self, numberOfBoids, width, height, map) :
        self.numberOfBoids = numberOfBoids
        self.map = map
        self.leader = Boid(*np.random.rand(2)*1000, width, height, self.map)
        self.boids = [Boid(*np.random.rand(2)*1000, width, height, self.map, self.leader) for _ in range(numberOfBoids-1)]
        self.barycenter = Vector(0,0)
        
    
    def update_leader(self):
        self.leader.edges()
        self.leader.apply_behaviour(self.boids)
        self.leader.update("boids")
        self.leader.show(self.boids, self.barycenter, leader = True)
        
    
    def update_boids(self):
        for boid in self.boids:
            boid.edges()
            boid.apply_behaviour(self.boids)
            boid.update("boids")
            boid.show(self.boids, self.barycenter)
        
            
    def get_barycenter(self):
        barycenter = Vector(0,0)
        print(barycenter)
        for boid in self.boids:
            barycenter += boid.position
        barycenter += self.numberOfBoids/2*self.leader.position
        barycenter /= self.numberOfBoids+1
        self.barycenter = barycenter
    
    
    #def draw_barycenter(self, screen):
    #    self.get_barycenter()
    #    pygame.draw.circle(screen, "green", (int(self.barycenter[0]), int(self.barycenter[1])), 5)
         

        
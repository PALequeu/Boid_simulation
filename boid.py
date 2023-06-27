from p5 import Vector
import numpy as np
import random as rd

import pygame

class Boid():

    def __init__(self, x, y, width, height, map, leader = None):
        self.position = Vector(x, y)
        vec = (np.random.rand(2) - 0.5)*10
        #self.velocity = Vector(*vec)
        self.velocity = Vector(0.1,0.1)

        vec = (np.random.rand(2) - 0.5)/2
        self.acceleration = Vector(*vec)
        self.max_force = 0.5
        self.max_speed = 2
        self.perception = 99
        
        self.leader = leader

        self.width = width
        self.height = height
        
        self.map = map


    def update(self,mode):
        distance = np.linalg.norm(self.position - self.leader.position)
        print(distance)
        if mode == "boids":
            self.position += self.velocity
            velocity = self.velocity+self.acceleration
            if distance > 100:
                velocity = velocity*float(np.exp(-(10/(distance-100))))
            if distance == 100:
                velocity = 0
            #if distance < 100:
            #    velocity = velocity*float(np.exp(-(10/(distance))))

            self.velocity = velocity
            print(self.velocity)
            #limit
            if np.linalg.norm(self.velocity) > self.max_speed:
                self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

            self.acceleration = Vector(*np.zeros(2))
            
    
            
    def show(self,boids, barycenter, leader = False):
        boid_pos = pygame.Vector2(self.position.x, self.position.y)
        if(not leader):
            pygame.draw.circle(self.map, "red", boid_pos, 10)
            #pygame.draw.circle(self.map, "red", boid_pos, 100, 1)
            
        else :
            pygame.draw.circle(self.map, "blue", boid_pos, 10)
            #pygame.draw.circle(self.map, "blue", boid_pos, 100, 1)
        #if self.leader != None :
            #cohes = self.cohesion()
            #align = self.align(boids)
            #self.drawArrow("red",align)
            #self.drawArrow("blue",cohes)
            
        
        #sep = self.separation(boids)
        #self.drawArrow("green",sep)
 


    def apply_behaviour(self, boids):
        if self.leader != None :
            #alignment = self.align(boids)
            cohesion = self.cohesion()
            #self.acceleration += alignment
            self.acceleration += cohesion
       
        separation = self.separation(boids)
        self.acceleration += separation

    def edges(self):
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height

    def align(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        avg_vector = Vector(*np.zeros(2))
        i=0
        for boid in boids:
            i+=1
            if np.linalg.norm(boid.position - self.position) < self.perception:
                avg_vector += boid.velocity
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = Vector(*avg_vector)
            avg_vector = (avg_vector /  np.linalg.norm(avg_vector)) * self.max_speed
            steering = avg_vector - self.velocity

        return steering

    def cohesion(self):
        # steering = Vector(*np.zeros(2))
        # total = 0
        # center_of_mass = Vector(*np.zeros(2))
        # i=0
        # green_close = False
        # for boid in boids:
        #     i+=1
        #     if np.linalg.norm(boid.position - self.position) < self.perception:
        #         if i == 1:
        #             green_close=True
        #             for j in range (0,19):
        #                 center_of_mass += boid.position
        #                 total+=20
        #         center_of_mass += boid.position
        #         total += 1
        
        # if total > 0:
        #     center_of_mass /= total
        #     center_of_mass = Vector(*center_of_mass)
        # print("barycenter",barycenter,"self.position",self.position)
        # barycenter = Vector(barycenter.x, barycenter.y)
       
      
        vec_to_com = self.leader.position - self.position
        if np.linalg.norm(vec_to_com) > 0:
            vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
        steering = vec_to_com - self.velocity
        if np.linalg.norm(steering)> self.max_force:
            steering = (steering /np.linalg.norm(steering)) * self.max_force
        #steering = steering*int(distance)
        #print("cohesion", steering)
        distance = np.linalg.norm(self.position - self.leader.position)
        if distance > 100:
            steering *= float(np.exp(-(10/(distance-100))))
        else :
            steering = -steering
        return steering
    

    def separation(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        avg_vector = Vector(*np.zeros(2))
        i=0
        
        #for boids
        for boid in boids:
            distance = np.linalg.norm(boid.position - self.position)
            if self.position != boid.position and distance < self.perception:
                diff = (self.position - boid.position) * float(np.exp((10/(distance))))
                #diff /= distance
                avg_vector += diff*(self.perception-distance)
                total += 1
        #for leader
        if self.leader != None:
            distance = np.linalg.norm(self.leader.position - self.position)
            if self.position != self.leader.position and distance < self.perception:
                diff = self.position - self.leader.position
                diff *= float(np.exp((10/(distance))))
                avg_vector += diff*(self.perception-distance)
                total += 1
                
        if total > 0:
            avg_vector /= total
            avg_vector = Vector(*avg_vector)
            if np.linalg.norm(steering) > 0:
                avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed
            steering = avg_vector - self.velocity
            if np.linalg.norm(steering) > 1*self.max_force:
                steering = (steering /np.linalg.norm(steering)) *1*self.max_force
        #print("separation", steering)
        return steering



    
    def drawArrow(self,color,vect):
            effect = pygame.Vector2(vect.x, vect.y)
            boid_pos = pygame.Vector2(self.position.x, self.position.y)
            pygame.draw.line(self.map,color,boid_pos,effect*100+boid_pos)
            # pygame.stroke(my_color)
            # fill(my_color)
            # line(self.position,vect*100+self.position)
    
    def Leader(self,mode):
        if (mode == "random"):
            self.acceleration= Vector(rd.uniform(-1,1),rd.uniform(-1,1))
        if (mode == "carré"): 
            if self.acceleration == None: 
                self.acceleration = Vector(12)
                if np.linalg.norm(self.acceleration) > self.max_force:
                    self.acceleration = (self.acceleration /np.linalg.norm(self.acceleration)) * self.max_force 

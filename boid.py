from p5 import *
import numpy as np
import random as rd

class Boid():

    def __init__(self, x, y, width, height):
        self.position = Vector(x, y)
        vec = (np.random.rand(2) - 0.5)*10
        self.velocity = Vector(*vec)

        vec = (np.random.rand(2) - 0.5)/2
        self.acceleration = Vector(*vec)
        self.max_force = 0.5
        self.max_speed = 5
        self.perception = 50

        self.width = width
        self.height = height
    


    def update(self,mode):
        if mode == "boids":
            self.position += self.velocity
            self.velocity += self.acceleration
            #limit
            if np.linalg.norm(self.velocity) > self.max_speed:
                self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

            self.acceleration = Vector(*np.zeros(2))
        if mode == "carré" : 
            #comportement du master
            x,y = self.position.x,self.position.y
            if x > 950: 
                self.acceleration.x = -1
            if x < 50:
                self.acceleration.x = 1
            if y > 950:
                self.acceleration.y = -1
            if y < 50: 
                self.acceleration.y = 1
            if np.linalg.norm(self.acceleration) > self.max_force:
                self.acceleration = (self.acceleration /np.linalg.norm(self.acceleration)) * self.max_force            
            self.position += self.velocity
            self.velocity += self.acceleration
            #limit
            if np.linalg.norm(self.velocity) > self.max_speed:
                self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

            self.acceleration = Vector(*np.zeros(2))
    def show(self,count,boids):
        stroke(255)
        fill(255)
        circle((self.position.x, self.position.y), radius=10)
        if (True):#count == 1):
            align = self.align(boids)
            cohes = self.cohesion(boids)
            sep = self.separation(boids)
            att = self.attraction(boids)
            self.drawArrow(Color(255,0,0),align)
            self.drawArrow(Color(0,0,255),cohes)
            self.drawArrow(Color(0,255,0),sep)
            self.drawArrow(Color(100,100,100),att)
    def leadershow(self):
        stroke(Color(255,0,0))
        fill(Color(0,255,0))
        circle((self.position.x, self.position.y), radius=10)


    def apply_behaviour(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        attraction = self.attraction(boids)

        self.acceleration += attraction
        self.acceleration += alignment
        self.acceleration += cohesion
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

    def cohesion(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        center_of_mass = Vector(*np.zeros(2))
        i=0
        green_close = False
        for boid in boids:
           i+=1
           if np.linalg.norm(boid.position - self.position) < self.perception:
                if i == 1:
                    green_close=True
                    for j in range (0,19):
                        center_of_mass += boid.position
                        total+=20
                center_of_mass += boid.position
                total += 1
        if total > 0:
            center_of_mass /= total
            center_of_mass = Vector(*center_of_mass)
            vec_to_com = center_of_mass - self.position
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
            steering = vec_to_com - self.velocity
            if np.linalg.norm(steering)> self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force*(0.3+0.7*green_close)

        return steering

    def separation(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        avg_vector = Vector(*np.zeros(2))
        i=0
        for boid in boids:
            distance = np.linalg.norm(boid.position - self.position)
            if self.position != boid.position and distance < self.perception:
                diff = self.position - boid.position
                diff /= distance
                avg_vector += diff*(self.perception-distance)
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = Vector(*avg_vector)
            if np.linalg.norm(steering) > 0:
                avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed
            steering = avg_vector - self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force
        return steering
    def attraction(self, boids): 
        #force d'attraction au master, qui change assez peu le comportement du flock
        steering = Vector(*np.zeros(2))
        boid = boids[0]
        distance = np.linalg.norm(boid.position - self.position)
        if self.position != boid.position and distance < self.perception:
            diff = self.position - boid.position
            diff /= distance
            if np.linalg.norm(steering) > 0:
                diff = (diff / np.linalg.norm(diff)) * self.max_speed
            steering = diff - self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering /np.linalg.norm(steering)) * self.max_force
        return steering
    def drawArrow(self,my_color,vect):
            stroke(my_color)
            fill(my_color)
            line(self.position,vect*100+self.position)
    def Leader(self,mode):
        if (mode == "random"):
            self.acceleration= Vector(rd.uniform(-1,1),rd.uniform(-1,1))
        if (mode == "carré"): 
            if self.acceleration == None: 
                self.acceleration = Vector(12)
                if np.linalg.norm(self.acceleration) > self.max_force:
                    self.acceleration = (self.acceleration /np.linalg.norm(self.acceleration)) * self.max_force 

from p5 import setup, draw, size, background, run, color, Vector
import numpy as np
import pygame
from boid import Boid
from flock import Flock

# width = 1000
# height = 1000

# pygame.init()
# font = pygame.font.Font("arial.ttf", 25)

# def setup():
#     #this happens just once
#     size(width, height) #instead of create_canvas


# def draw():
#     global flock
#     count = 0
#     leadi= 0
#     background(30, 30, 47)

#     for boid in flock:
#         count+=1
#         leadi+=1
#         if (leadi == 1):
#             boid.edges()
#             boid.Leader("carré")
#             boid.update("carré")
#             boid.leadershow()

#         else:
#             boid.edges()
#             boid.apply_behaviour(flock)
#             boid.update("boids")
#             boid.show(count,flock)

# #run(frame_rate=100)
# #run(frame_rate=200)
# run()

class game() :
    def __init__(self, numberOfBoids = 5, w=800, h=800 ):
        self.w = w
        self.h = h
        self.start_ticks = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.map = pygame.display.set_mode((self.w, self.h))
        self.flock = Flock(numberOfBoids,w ,h, self.map) 
        self.dt = 0
        
    def play(self):
        running = True
        player_pos = pygame.Vector2(self.map.get_width() / 2, self.map.get_height() / 2)
        while running :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.map.fill("black")
            
            
            #draw the leader
            #self.flock.update_leader()
            boid_pos = pygame.Vector2(self.flock.leader.position.x, self.flock.leader.position.y)
            pygame.draw.circle(self.map, "blue", boid_pos, 10)
            #pygame.draw.circle(self.map, "blue", boid_pos, 100, 1)
            #self.flock.update_leader()
            
            #draw the boids
            self.flock.update_boids()
            
            #draw the barycenter
            #self.flock.draw_barycenter(self.map)
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                self.flock.leader.position.y -= 100 * self.dt
            if keys[pygame.K_s]:
                self.flock.leader.position.y += 100 * self.dt
            if keys[pygame.K_q]:
                self.flock.leader.position.x -= 100 * self.dt
            if keys[pygame.K_d]:
                self.flock.leader.position.x += 100 * self.dt
                
            pygame.display.flip()
            
            self.dt = self.clock.tick(60) / 1000
        pygame.quit()
        
    

if __name__ == "__main__":
    game = game(10)
    game.play()

                
    
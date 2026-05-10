import warnings
warnings.filterwarnings('ignore', category=UserWarning)
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import pygame.math as math
import random as r

class Bird:
    BASE_SHAPE = None
    BASE_COLOR = None
    r_sight_sq = 0

    def __init__(self, pos: math.Vector2, vel: math.Vector2):
        self.pos = pos
        self.vel = vel

    def update(self, boid_list):
        pass

    def draw(self, surface):
        angle = math.Vector2(0, -1).angle_to(self.vel)
        rotated_shape = [p.rotate(angle) + self.pos for p in self.BASE_SHAPE]
        pygame.draw.polygon(surface, self.BASE_COLOR, rotated_shape)

class Boid(Bird):
    BASE_SHAPE = [math.Vector2(0, -4), math.Vector2(-2, 2), math.Vector2(2, 2)]
    BASE_COLOR = (0, 255, 100)

    r_sight = 75
    r_sight_sq = r_sight * r_sight
    r_near = 25
    r_near_sq = r_near * r_near
    max_vel = 4
    max_vel_sq = max_vel * max_vel

    w_sep = 0.1
    w_align = 0.05
    w_coh = 0.01
    w_flee = 100

    def update(self, boid_list, pred_list):
        neighbors = [other for other in boid_list
                     if other != self
                     and self.pos.distance_squared_to(other.pos) < self.r_sight_sq]

        if neighbors:
            # 1. separation (r_near)
            nears = [neighbor.pos for neighbor in neighbors
                     if self.pos.distance_squared_to(neighbor.pos) < self.r_near_sq]
            if nears:
                sep_vec = sum((self.pos - near_pos for near_pos in nears), math.Vector2())
                self.vel += sep_vec * self.w_sep

            # 2. alignment
            avg_vel = sum((neighbor.vel for neighbor in neighbors), math.Vector2()) / len(neighbors)
            self.vel += (avg_vel - self.vel) * self.w_align

            # 3. cohesion
            avg_pos = sum((neighbor.pos for neighbor in neighbors), math.Vector2()) / len(neighbors)
            self.vel += (avg_pos - self.pos) * self.w_coh

        # 4. Flee/Evade
        pred_in_sight = [pred for pred in pred_list
                    if self.pos.distance_squared_to(pred.pos) < self.r_sight_sq]
        if pred_in_sight:
            flee_vec = sum((self.pos - pred.pos for pred in pred_in_sight), math.Vector2())
            self.vel += flee_vec * self.w_flee

        # Normalize
        self.vel = self.vel.normalize() * self.max_vel \
            if self.vel.length_squared() > self.max_vel_sq else self.vel

        # Torus
        self.pos += self.vel
        self.pos.x %= W
        self.pos.y %= H

class Predator(Bird):
    BASE_SHAPE = [math.Vector2(0, -8), math.Vector2(-4, 4), math.Vector2(4, 4)]
    BASE_COLOR = (255, 0, 0)

    r_sight = 200
    r_sight_sq = r_sight * r_sight

    max_vel = 4.5
    max_vel_sq = max_vel * max_vel

    def update(self, boid_list):
        prey_pos = [other.pos for other in boid_list
                     if other != self
                     and self.pos.distance_squared_to(other.pos) < self.r_sight_sq]

        if prey_pos:
            # Chase
            avg_pos = sum(prey_pos, math.Vector2()) / len(prey_pos)
            self.vel += avg_pos - self.pos

        # Normalize
        self.vel = self.vel.normalize() * self.max_vel \
            if self.vel.length_squared() > self.max_vel_sq else self.vel

        # Torus
        self.pos += self.vel
        self.pos.x %= W
        self.pos.y %= H

pygame.init()

W, H = 800, 600
n_boids = 100
boids = [Boid(math.Vector2(r.randint(0, W-1), r.randint(0, H-1)),
              math.Vector2(0, -1).rotate(r.uniform(0, 180)))
         for _ in range(n_boids)]
n_preds = 1
preds = [Predator(math.Vector2(r.randint(0, W-1), r.randint(0, H-1)),
              math.Vector2(0, -1).rotate(r.uniform(0, 180)))
         for _ in range(n_preds)]

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('GUI')
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # --- update ---
    for boid in boids:
        boid.update(boids, preds)
        boid.draw(screen)

    # --- update preds ---
    for pred in preds:
        pred.update(boids)
        pred.draw(screen)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()

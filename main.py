import collections
import itertools
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from pygame.math import Vector2
import random as r
import math

def get_shortest_vec(pos1, pos2, W, H):
    dx = pos2.x - pos1.x
    dy = pos2.y - pos1.y

    if dx > W / 2: dx -= W
    elif dx < -W / 2: dx += W

    if dy > H / 2: dy -= H
    elif dy < -H / 2: dy += H

    return Vector2(dx, dy)

class Bird:
    BASE_SHAPE = None
    BASE_COLOR = None
    r_sight_sq = 0

    def __init__(self, pos: Vector2, vel: Vector2):
        self.pos = pos
        self.vel = vel

    def update(self, boid_list):
        pass

    def draw(self, surface):
        angle = Vector2(0, -1).angle_to(self.vel)
        rotated_shape = [p.rotate(angle) + self.pos for p in self.BASE_SHAPE]
        pygame.draw.polygon(surface, self.BASE_COLOR, rotated_shape)

class Boid(Bird):
    BASE_SHAPE = [Vector2(0, -4), Vector2(-2, 2), Vector2(2, 2)]
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
    w_avoid = 10

    def update(self, boid_list, pred_list=None, obstacle_list=None):
        neighbors = [other for other in boid_list
                     if other != self
                     and get_shortest_vec(self.pos, other.pos, W, H).length_squared() < self.r_sight_sq]

        if neighbors:
            # 1. separation (r_near)
            nears = [neighbor.pos for neighbor in neighbors
                     if get_shortest_vec(self.pos, neighbor.pos, W, H).length_squared() < self.r_near_sq]
            if nears:
                sep_vec = sum((get_shortest_vec(near_pos, self.pos, W, H) for near_pos in nears), Vector2())
                self.vel += sep_vec * self.w_sep

            # 2. alignment
            avg_vel = sum((neighbor.vel for neighbor in neighbors), Vector2()) / len(neighbors)
            self.vel += (avg_vel - self.vel) * self.w_align

            # 3. cohesion
            avg_dist = sum((get_shortest_vec(self.pos, neighbor.pos, W, H)
                            for neighbor in neighbors), Vector2()) / len(neighbors)
            self.vel += avg_dist * self.w_coh

        # 4. Flee/Evade
        if pred_list:
            pred_in_sight = [pred for pred in pred_list
                        if get_shortest_vec(self.pos, pred.pos, W, H).length_squared() < self.r_sight_sq]
            if pred_in_sight:
                flee_vec = sum((get_shortest_vec(pred.pos, self.pos, W, H) for pred in pred_in_sight), Vector2())
                self.vel += flee_vec * self.w_flee

        # 5. Steering (avoid obstacle)
        if obstacle_list:
            for obs in obstacle_list:
                to_obs = get_shortest_vec(self.pos, obs.pos, W, H)
                forward_dir = self.vel.normalize()
                forward_dist = to_obs.dot(forward_dir)
                if 0 < forward_dist < self.r_sight:
                    perp_dir = forward_dir.rotate(90)
                    lateral_dist = to_obs.dot(perp_dir)
                    if abs(lateral_dist) < obs.radius + 4:
                        turn_force = perp_dir * self.w_avoid
                        dist_force = max(1e-2, forward_dist - obs.radius - 4) # sharper steering if close

                        self.vel = forward_dir * self.max_vel
                        # opposite direction to obstacle
                        if lateral_dist > 0:
                            self.vel -= turn_force / dist_force
                        else:
                            self.vel += turn_force / dist_force
                        # ignore other obstacles after deciding what obs to avoid
                        break

                # Hard Resolution (force collision)
                actual_dist_sq = to_obs.length_squared()
                min_dist = obs.radius + 4
                if actual_dist_sq < min_dist * min_dist:
                    actual_dist = math.sqrt(actual_dist_sq)
                    overlap = min_dist - actual_dist
                    self.pos -= to_obs / actual_dist * overlap

        # Normalize
        self.vel = self.vel.normalize() * self.max_vel \
            if self.vel.length_squared() > self.max_vel_sq else self.vel

        # Torus
        self.pos += self.vel
        self.pos.x %= W
        self.pos.y %= H

class Predator(Bird):
    BASE_SHAPE = [Vector2(0, -8), Vector2(-4, 4), Vector2(4, 4)]
    BASE_COLOR = (255, 0, 0)

    r_sight = 200
    r_sight_sq = r_sight * r_sight

    max_vel = 4.5
    max_vel_sq = max_vel * max_vel

    def update(self, boid_list):
        prey_pos = [other.pos for other in boid_list
                     if other != self
                     and get_shortest_vec(self.pos, other.pos, W, H).length_squared() < self.r_sight_sq]

        if prey_pos:
            # Chase
            avg_dist = sum((get_shortest_vec(self.pos, pp, W, H)
                           for pp in prey_pos), Vector2()) / len(prey_pos)
            self.vel += avg_dist

        # Normalize
        self.vel = self.vel.normalize() * self.max_vel \
            if self.vel.length_squared() > self.max_vel_sq else self.vel

        # Torus
        self.pos += self.vel
        self.pos.x %= W
        self.pos.y %= H

class Obstacle:
    def __init__(self, pos, radius=3):
        self.pos = pos
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, (170, 170, 170), self.pos, self.radius)

pygame.init()

W, H = 800, 600
n_boids = 10
boids = [Boid(Vector2(r.randint(0, W-1), r.randint(0, H-1)),
              Vector2(0, -1).rotate(r.uniform(0, 180)))
         for _ in range(n_boids)]
n_preds = 1
preds = [Predator(Vector2(r.randint(0, W-1), r.randint(0, H-1)),
                  Vector2(0, -1).rotate(r.uniform(0, 180)))
         for _ in range(n_preds)]
n_obstacles = 20
obstacles = [Obstacle(Vector2(r.randint(0, W-1), r.randint(0, H-1)),
                      radius=15)
             for _ in range(n_obstacles)]

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('GUI')
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    grid = collections.defaultdict(list)
    GRID_SIZE = 75
    MAX_GX = math.ceil(W / GRID_SIZE)
    MAX_GY = math.ceil(H / GRID_SIZE)

    for boid in boids:
        gx = int(boid.pos.x // GRID_SIZE)
        gy = int(boid.pos.y // GRID_SIZE)
        grid[(gx, gy)].append(boid)

    # --- update ---
    for boid in boids:
        gx = int(boid.pos.x // GRID_SIZE)
        gy = int(boid.pos.y // GRID_SIZE)

        adjacent_boids = []
        for i, j in itertools.product([-1, 0, 1], repeat=2):
            wrap_x = (gx + i) % MAX_GX
            wrap_y = (gy + j) % MAX_GY
            adjacent_boids.extend(grid[(wrap_x, wrap_y)])

        boid.update(adjacent_boids, preds, obstacles)
        boid.draw(screen)

    # --- update preds ---
    for pred in preds:
        # Pos & Vel Calc (Vel: to render direction)
        last_pos = pred.pos
        curr_pos = Vector2(pygame.mouse.get_pos())
        curr_vel = curr_pos - last_pos

        pred.pos = curr_pos
        # Preventing reset to default direction when not moving
        pred.vel = pred.vel if curr_vel.length_squared() == 0 else curr_vel
        pred.draw(screen)

    for obs in obstacles:
        obs.draw(screen)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()

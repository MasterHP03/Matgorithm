import warnings

warnings.filterwarnings('ignore', category=UserWarning)
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from collections import deque
import pygame
from pygame.math import Vector2
import random as r

W, H = 800, 600
GRID_SIZE = 30
GW, GH = W // GRID_SIZE, H // GRID_SIZE

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid(r, c):
    return 0 <= r < GW and 0 <= c < GH

def find_path(snk: deque[Vector2], apl: Vector2):
    start = int(snk[0].x), int(snk[0].y)

    body_set = set((int(v.x), int(v.y)) for i, v in enumerate(snk) if i > 0)

    dq = deque()
    visited = {start}

    for dr, dc in directions:
        nr, nc = start[0] + dr, start[1] + dc
        if is_valid(nr, nc) and (nr, nc) not in body_set:
            dq.append(((nr, nc), Vector2(dr, dc)))
            visited.add((nr, nc))

    while dq:
        (r, c), start_dir = dq.popleft()

        if (r, c) == (int(apl.x), int(apl.y)):
            return start_dir

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if is_valid(nr, nc) and (nr, nc) not in body_set and (nr, nc) not in visited:
                visited.add((nr, nc))
                dq.append(((nr, nc), start_dir))

    return None

def survive(snk: deque[Vector2]):
    start = int(snk[0].x), int(snk[0].y)

    body_set = set((int(v.x), int(v.y)) for i, v in enumerate(snk) if i > 0)

    for dr, dc in directions:
        nr, nc = start[0] + dr, start[1] + dc
        if is_valid(nr, nc) and (nr, nc) not in body_set:
            return Vector2(dr, dc)

    return None


pygame.init()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('GUI')
clock = pygame.time.Clock()

snake = deque()
snake.append(Vector2(r.randint(0, GW - 1), r.randint(0, GH - 1)))
direction = Vector2(-1, 0)

apple = Vector2(r.randint(0, GW - 1), r.randint(0, GH - 1))
while apple == snake[0]:
    apple = Vector2(r.randint(0, GW - 1), r.randint(0, GH - 1))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for n, pos in enumerate(snake):
        pygame.draw.rect(screen, (0, 255 if n == 0 else 200, 100),
                         (pos.x * GRID_SIZE, pos.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.circle(screen, (255, 0, 0),
                       (apple.x * GRID_SIZE + GRID_SIZE / 2, apple.y * GRID_SIZE + GRID_SIZE / 2),
                       GRID_SIZE / 2)

    direction = find_path(snake, apple)
    if direction:
        snake.appendleft(snake[0] + direction)
        if snake[0] != apple:
            snake.pop()
        else:
            full_body = set((int(v.x), int(v.y)) for v in snake)
            apple = Vector2(r.randint(0, GW - 1), r.randint(0, GH - 1))
            while (apple.x, apple.y) in full_body:
                apple = Vector2(r.randint(0, GW - 1), r.randint(0, GH - 1))
    else:
        direction = survive(snake)
        if direction:
            snake.appendleft(snake[0] + direction)
            snake.pop()
        else:
            pass

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

from collections import deque

import numpy as np
import random


def generate_real_maze(width, height, sr, sc):
    grid = np.zeros((height + 2, width + 2), dtype=int)

    # 1. 방향 정의
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def is_valid(r, c):
        return 1 <= r < height + 1 and 1 <= c < width + 1

    # 2. 시작점 설정. (0, 0)부터 시작해서 길(1) 뚫기
    r, c = sr, sc
    dist = 0
    grid[r][c] = 4

    stack = [(r, c, dist)]

    max_r, max_c, max_dist = 0, 0, 0

    while stack:
        r, c, dist = stack[-1]
        if dist > max_dist:
            max_r, max_c, max_dist = r, c, dist

        # 3. 갈 수 있는 칸 중, 인접한 셀이 다 벽인 칸 찾기
        valid_neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and grid[nr][nc] == 0:
                count_neigh = 0
                for ddr, ddc in directions:
                    nnr, nnc = nr + ddr, nc + ddc
                    # 이미 뚫린 칸이 없어야 함 (단, 지나온 길 자체는 벽이 아니니 1칸은 유예.)
                    if is_valid(nnr, nnc) and grid[nnr][nnc] != 0:
                        count_neigh += 1
                if count_neigh <= 1:
                    valid_neighbors.append((nr, nc, dr, dc))

        if valid_neighbors:
            # 4. 갈 곳 있다면 랜덤 선택 전진
            nr, nc, dr, dc = random.choice(valid_neighbors)
            grid[nr][nc] = 1
            stack.append((nr, nc, dist + 1))
        else:
            # 5. 사방이 막혔다면 뒤로 가기 (백트래킹)
            stack.pop()

    grid[max_r][max_c] = 2

    return grid


def find_path(grid, start):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def is_valid(r, c):
        return 1 <= r < grid.shape[0] - 1 and 1 <= c < grid.shape[1] - 1

    r, c = start
    dist = 0
    dq = deque([(r, c, dist)])

    parent_map: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

    er, ec = 0, 0

    while dq:
        r, c, dist = dq.popleft()

        if grid[r][c] == 2:
            er, ec = r, c
            break

        for i in range(4):
            dr, dc = directions[i]
            nr, nc = r + dr, c + dc

            if is_valid(nr, nc) and grid[nr][nc] != 0 and (nr, nc) not in parent_map:
                parent_map[(nr, nc)] = (r, c)
                dq.append((nr, nc, dist + 1))

    if (er, ec) == (0, 0):
        return None

    result_grid = grid.copy()
    pr, pc = er, ec
    while parent_map[(pr, pc)] is not None:
        pr, pc = parent_map[(pr, pc)]
        if (pr, pc) != start:
            result_grid[pr][pc] = 3

    return result_grid


w, h = 41, 41
v_start = 1, 1
board = generate_real_maze(w, h, v_start[0], v_start[1])
for rows in board:
    for e in rows:
        print('\u2B1B' if e == 0 else '\U0001F7E8' if e == 2 else '\U0001F7E6' if e == 4 else '\u2B1C', end=' ')
    print()
print()

result_board = find_path(board, v_start)
if result_board is None:
    print("No path")
else:
    for rows in result_board:
        for e in rows:
            print('\u2B1B' if e == 0 else '\U0001F7E8' if e == 2 else '\U0001F7E6' if e == 4 else '\U0001F7E9' if e == 3 else '\u2B1C', end=' ')
        print()
print()

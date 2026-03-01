import pygame
import sys
import heapq
import time

pygame.init()

WIDTH = 600
ROWS = 20
CELL_SIZE = WIDTH // ROWS

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding - A*")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (200, 200, 200)

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = WHITE
        self.neighbors = []
        self.g = float("inf")
        self.f = float("inf")
        self.parent = None

    def __lt__(self, other):
        return False

    def is_wall(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE

    def make_wall(self):
        self.color = BLACK

    def make_start(self):
        self.color = GREEN

    def make_goal(self):
        self.color = RED

    def make_path(self):
        self.color = BLUE

    def make_open(self):
        self.color = YELLOW

    def make_closed(self):
        self.color = GREY

    def draw(self):
        pygame.draw.rect(
            WIN,
            self.color,
            (self.col * CELL_SIZE, self.row * CELL_SIZE,
             CELL_SIZE, CELL_SIZE)
        )

def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def make_grid():
    return [[Node(i, j) for j in range(ROWS)] for i in range(ROWS)]

def draw_grid():
    for i in range(ROWS):
        pygame.draw.line(WIN, GREY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        pygame.draw.line(WIN, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH))

def draw(grid):
    WIN.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw()
    draw_grid()
    pygame.display.update()

def update_neighbors(grid):
    for row in grid:
        for node in row:
            node.neighbors = []
            r, c = node.row, node.col

            if r < ROWS - 1 and not grid[r+1][c].is_wall():
                node.neighbors.append(grid[r+1][c])
            if r > 0 and not grid[r-1][c].is_wall():
                node.neighbors.append(grid[r-1][c])
            if c < ROWS - 1 and not grid[r][c+1].is_wall():
                node.neighbors.append(grid[r][c+1])
            if c > 0 and not grid[r][c-1].is_wall():
                node.neighbors.append(grid[r][c-1])

def reconstruct_path(end):
    while end.parent:
        end = end.parent
        if end.parent:
            end.make_path()

def a_star(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    start.g = 0

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            reconstruct_path(goal)
            return

        current.make_closed()

        for neighbor in current.neighbors:
            temp_g = current.g + 1

            if temp_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = temp_g
                f = neighbor.g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))
                neighbor.make_open()

        draw(grid)

def main():
    grid = make_grid()
    start = None
    goal = None

    run = True
    while run:
        draw(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                row = pygame.mouse.get_pos()[1] // CELL_SIZE
                col = pygame.mouse.get_pos()[0] // CELL_SIZE
                node = grid[row][col]

                if not start:
                    start = node
                    start.make_start()
                elif not goal:
                    goal = node
                    goal.make_goal()
                else:
                    node.make_wall()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and goal:
                    update_neighbors(grid)
                    a_star(grid, start, goal)

                if event.key == pygame.K_c:
                    grid = make_grid()
                    start = None
                    goal = None

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
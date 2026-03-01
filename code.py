import itertools
import tkinter as tk
from tkinter import simpledialog
import heapq
import time

WIDTH = 600
ROWS = 20
CELL_SIZE = WIDTH // ROWS

WHITE = "white"
BLACK = "black"
GREEN = "green"
RED = "red"
BLUE = "blue"
YELLOW = "yellow"
GREY = "light grey"

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = WHITE
        self.neighbors = []
        self.g = float("inf")
        self.parent = None

    def is_wall(self):
        return self.color == BLACK

    def reset(self):
        if self.color not in [GREEN, RED, BLACK]:
            self.color = WHITE
        self.g = float("inf")
        self.parent = None

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return (self.row, self.col) == (other.row, other.col)

def heuristic(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def make_grid():
    return [[Node(i, j) for j in range(ROWS)] for i in range(ROWS)]

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

def reconstruct_path(goal, path_color=BLUE):
    while goal.parent:
        goal = goal.parent
        if goal.parent:
            goal.color = path_color

def a_star(grid, start, goal):
    counter = itertools.count()
    open_set = []
    heapq.heappush(open_set, (0, next(counter), start))
    start.g = 0
    nodes = 0
    start_time = time.time()

    while open_set:
        current = heapq.heappop(open_set)[2]

        if current == goal:
            reconstruct_path(goal, BLUE)
            return nodes, (time.time() - start_time) * 1000

        nodes += 1
        current.color = GREY

        for neighbor in current.neighbors:
            temp_g = current.g + 1
            if temp_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = temp_g
                f = neighbor.g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, next(counter), neighbor))
                if neighbor != goal:
                    neighbor.color = YELLOW
    return 0, 0

def greedy(grid, start, goal):
    counter = itertools.count()
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), next(counter), start))
    visited = set()
    nodes = 0
    start_time = time.time()

    while open_set:
        current = heapq.heappop(open_set)[2]

        if current == goal:
            reconstruct_path(goal, "purple")
            return nodes, (time.time() - start_time) * 1000

        visited.add(current)
        nodes += 1
        current.color = GREY

        for neighbor in current.neighbors:
            if neighbor not in visited:
                neighbor.parent = current
                heapq.heappush(open_set, (heuristic(neighbor, goal), next(counter), neighbor))
                if neighbor != goal:
                    neighbor.color = YELLOW
    return 0, 0

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding Agent - Tkinter")

        self.canvas = tk.Canvas(root, width=WIDTH, height=WIDTH)
        self.canvas.pack()

        self.info = tk.Label(root, text="Nodes: 0   Time: 0 ms")
        self.info.pack()

        self.grid = make_grid()
        self.start = None
        self.goal = None

        self.canvas.bind("<Button-1>", self.handle_click)
        self.root.bind("<Return>", self.handle_run)  # Press Enter to run

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for row in self.grid:
            for node in row:
                x1 = node.col * CELL_SIZE
                y1 = node.row * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=node.color,
                                             outline="grey")
        self.root.update()

    def handle_click(self, event):
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE
        node = self.grid[row][col]

        if not self.start:
            self.start = node
            node.color = GREEN
        elif not self.goal:
            self.goal = node
            node.color = RED
        else:
            node.color = BLACK

        self.draw()

    def reset_path(self):
        for row in self.grid:
            for node in row:
                if node.color not in [BLACK, GREEN, RED]:
                    node.color = WHITE
                node.g = float("inf")
                node.parent = None

    def handle_run(self, event):
        if self.start and self.goal:
            algo = simpledialog.askstring("Algorithm", "Which algorithm? (A* or Greedy)")
            if not algo:
                return
            algo = algo.lower()
            self.reset_path()
            update_neighbors(self.grid)
            if algo in ['a*', 'astar']:
                nodes, t = a_star(self.grid, self.start, self.goal)
            elif algo == 'greedy':
                nodes, t = greedy(self.grid, self.start, self.goal)
            else:
                self.info.config(text="Invalid algorithm!")
                return
            self.info.config(text=f"Nodes: {nodes}   Time: {round(t,2)} ms")
            self.draw()

root = tk.Tk()
app = App(root)
root.mainloop()
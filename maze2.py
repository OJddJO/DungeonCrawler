# df_maze.py
import random

class Cell:
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def has_all_walls(self):
        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:
    def __init__(self, nx, ny, ix=0, iy=0):
        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

    def create_matrix(self):
        maze = []
        maze.append(['#' for i in range(self.nx * 2 + 1)])
        for y in range(self.ny):
            maze_row = ['#']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append('.')
                    maze_row.append('#')
                else:
                    for i in range(2):
                        maze_row.append('.')
            maze.append(maze_row)
            maze_row = ['#']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    for i in range(2):
                        maze_row.append('#')
                else:
                    maze_row.append('.')
                    maze_row.append('#')
            maze.append(maze_row)

        return maze

    def find_valid_neighbours(self, cell):
        delta = [
            ('W', (-1, 0)),
            ('E', (1, 0)),
            ('S', (0, 1)),
            ('N', (0, -1))
        ]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.maze_map[x2][y2]
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def make_maze(self):
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.maze_map[self.ix][self.iy]
        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                current_cell = cell_stack.pop()
                continue

            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1


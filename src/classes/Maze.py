import random

class Cell:
    """A cell in the maze."""
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """Initialize the cell at (x,y). At first it is surrounded by walls."""
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def has_all_walls(self):
        """Returns true if the cell still has all its walls."""
        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        """Knock down the wall between cells self and other."""
        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:
    """A Maze, represented as a grid of cells."""
    def __init__(self, nx, ny, ix=0, iy=0):
        """Initialize the maze grid. nx and ny are the size of the grid,"""
        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

    def create_matrix(self):
        """Create a matrix of the maze with ASCII characters"""
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
        """Return a list of unvisited neighbours to cell."""
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
        """Make a maze, with depth-first search"""
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

if __name__ == "__main__": #testing
    maze = Maze(20, 10)
    maze.make_maze()
    for element in maze.create_matrix():
        print(element)
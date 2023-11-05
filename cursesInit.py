import curses
from curses import textpad
from classes.Map import *
import time

colorDict = {
    '#': 1,
    '.': 7,
    'C': 2,
    'G': 3,
    'S': 2,
    '@': 5,
    'O': 6,
    'M': 4,
    '$': 2,
    ' ': 7
}

charDict = {
    '#': ' ',
    '.': ' ',
    'C': 'C',
    'G': 'G',
    'S': 'S',
    '@': '@',
    'O': 'O',
    'M': 'M',
    '$': '$',
    ' ': ' '
}

screen = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_BLACK)
screen.clear()
screen.refresh()

def printMap(map):
    textpad.rectangle(screen, 2, 2, 24, 64)
    for i, rows in enumerate(map):
        for j, element in enumerate(rows):
            screen.addstr(i + 3, j + 3, charDict[element], curses.color_pair(colorDict[element]))
    screen.refresh()

def printMenu(menu):
    for i, element in enumerate(menu):
        screen.addstr(i + 3, 3, element, curses.color_pair(7))
    screen.refresh()

player = Player("warrior")
map = Lobby(player)

printMap(map.colorMap(mist = False))

time.sleep(2)
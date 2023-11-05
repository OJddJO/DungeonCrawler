import curses
from curses import textpad
from classes.Map import *
import time

screen = curses.initscr()
screen.clear()

textpad.rectangle(screen, 2, 2, 22, 62)

screen.refresh()

def printMain(text):
    screen.addstr(3, 3, text)
    screen.refresh()

player = Player("warrior")
map = Lobby(player)

printMain(map.__str__())

time.sleep(2)
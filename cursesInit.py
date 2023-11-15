import curses
from curses import textpad

screen = curses.initscr()
screen.clear()
# curses.resize_term(52, 186)
curses.curs_set(0)
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)
mainWin = curses.newwin(41, 120, 1, 1) #size 40, 120
statsWin = curses.newwin(41, 60, 1, 125) #size 40, 60
infoWin = curses.newwin(7, 183, 43, 1) #size 6, 183


def refreshMain():
    mainWin.refresh()

def refreshStats():
    statsWin.refresh()

def refreshInfo():
    infoWin.refresh()

def drawOutlines():
    textpad.rectangle(screen, 0, 0, 41, 121) #main rectangle
    textpad.rectangle(screen, 0, 124, 41, 184) # stats rectangle
    textpad.rectangle(screen, 42, 0, 49, 184) # info rectangle

def refreshAll():
    mainWin.refresh()
    statsWin.refresh()
    infoWin.refresh()
    textpad.rectangle(screen, 0, 0, 41, 121) #main rectangle
    textpad.rectangle(screen, 0, 124, 41, 184) # stats rectangle
    textpad.rectangle(screen, 42, 0, 49, 184) # info rectangle
    screen.refresh()


def printMap(matrix):
    for i, row in enumerate(matrix):
        for j, element in enumerate(row): #element is a tuple (char, color)
            print(element)
            mainWin.addch(i, j, element[0], curses.color_pair(element[1]))
    mainWin.refresh()

infoList = []
def printInfo(string):
    if len(infoList) <= 10:
        infoList.pop(0)
    infoList.append(string)
    for i, row in enumerate(infoList):
        for j, element in enumerate(row):
            infoWin.addch(i, j, element)

if __name__ == "__main__":
    import time
    from classes.Map import Lobby, Room
    from classes.Player import Player

    refreshAll()
    # room = Room(Player("warrior"), 1, Lobby(Player("warrrior"))).colorMap()
    room = Lobby(Player()).colorMap(mist=False)
    printMap(room)
    time.sleep(5)
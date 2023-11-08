import curses
from curses import textpad

screen = curses.initscr()
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
mainWin = curses.newwin(40, 120, 1, 1)
statsWin = curses.newwin(40, 60, 1, 125)
infoWin = curses.newwin(8, 184, 43, 0)


def printOutlines():
    textpad.rectangle(screen, 0, 0, 42, 122) #main rectangle
    textpad.rectangle(screen, 0, 124, 42, 184) # inventory rectangle
    textpad.rectangle(screen, 43, 0, 50, 182) # info rectangle
    screen.refresh()
    mainWin.refresh()
    statsWin.refresh()
    infoWin.refresh()


def printList(matrix):
    for i, row in enumerate(matrix):
        for j, element in enumerate(row):
            mainWin.addstr(1+i, 1+j, element[0], curses.color_pair(element[1]))
    mainWin.refresh()

if __name__ == "__main__":
    import time
    printOutlines()
    time.sleep(2)
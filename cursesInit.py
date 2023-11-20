import curses
from curses import textpad

screen = curses.initscr()
screen.clear()
screen.keypad(True)
mainWin = curses.newwin(42, 121, 1, 1) #size 41, 121
statsWin = curses.newwin(42, 60, 1, 125) #size 41, 61
infoWin = curses.newwin(7, 183, 43, 1) #size 6, 183
curses.curs_set(0)
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) #wall (black on white)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) #yellow
curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK) #magenta
curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK) #red
curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK) #green
curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK) #cyan
curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK) #blue
curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK) #none
curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLACK) # for text base color (white on black)


def clearMain():
    mainWin.clear()
    mainWin.refresh()

def clearStats():
    statsWin.clear()
    statsWin.refresh()

def clearInfo():
    global infoList
    infoList = []
    infoWin.clear()
    infoWin.refresh()

def clearAll():
    clearMain()
    clearStats()
    clearInfo()

def drawOutlines():
    textpad.rectangle(screen, 0, 0, 42, 122) #main rectangle
    textpad.rectangle(screen, 0, 124, 42, 184) # stats rectangle
    textpad.rectangle(screen, 42, 0, 49, 184) # info rectangle

def refreshAll():
    mainWin.refresh()
    statsWin.refresh()
    infoWin.refresh()
    textpad.rectangle(screen, 0, 0, 42, 122) #main rectangle
    textpad.rectangle(screen, 0, 124, 42, 184) # stats rectangle
    textpad.rectangle(screen, 43, 0, 50, 184) # info rectangle
    screen.refresh()


def printMap(matrix):
    for i, row in enumerate(matrix):
        for j, element in enumerate(row): #element is a tuple (char, color)
            mainWin.addch(i, j, element[0], curses.color_pair(element[1]))
    mainWin.refresh()

def printText(win, line, text):
    cursor = 0
    for element in text:
        col = curses.color_pair(element[1])
        if element[2] == "bold":
            col += curses.A_BOLD
        elif element[2] == "italic":
            col += curses.A_ITALIC
        win.addstr(line, cursor, element[0], col)
        cursor += len(element[0])
    win.refresh()

infoList = [] #list ex: [[("You", 3, "bold"), (" are ", 9, None), ("burning", 4, None), (" for 2 turns", 9, None)]] list of list of tuple that contain a string, a color code and a type
def printInfo(text):
    infoList.append(text) #need to be [("string", color, type of text)]
    infoList.pop(0) if len(infoList) > 6 else None
    for i, text in enumerate(infoList):
        printText(infoWin, 6-i, text)


if __name__ == "__main__":
    import time
    from classes.Map import Lobby, Room
    from classes.Player import Player

    refreshAll()
    # room = Room(Player("warrior"), 1, Lobby(Player("warrrior"))).colorMap()
    room = Lobby(Player()).colorMap(mist=False)
    printMap(room)
    printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to continue", 9, None)])
    printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to continue", 9, None)])
    printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to continue", 9, None)])
    printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to continue", 9, None)])
    printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to continue", 9, None)])
    printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to continue", 9, None)])
    printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to continue", 9, None)])
    time.sleep(5)
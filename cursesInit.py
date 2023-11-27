import curses
from curses import textpad

screen = curses.initscr()
screen.clear()
# screen.keypad(True)
mainWin = curses.newwin(43, 123, 0, 0) #size 41, 121
mainWin.border()
statsWin = curses.newwin(43, 61, 0, 124) #size 41, 59
statsWin.border()
infoWin = curses.newwin(8, 185, 43, 0) #size 6, 183
infoWin.border()    
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
    mainWin.border()
    mainWin.refresh()

def clearStats():
    statsWin.clear()
    statsWin.border()
    statsWin.refresh()

def clearInfo():
    global infoList
    infoList = []
    infoWin.clear()
    infoWin.border()
    infoWin.refresh()

def clearAll():
    clearMain()
    clearStats()
    clearInfo()

def refreshAll():
    mainWin.refresh()
    statsWin.refresh()
    infoWin.refresh()


def printMap(matrix):
    for i, row in enumerate(matrix, 1):
        for j, element in enumerate(row, 1): #element is a tuple (char, color)
            mainWin.addch(i, j, element[0], curses.color_pair(element[1]))
    mainWin.refresh()

def printText(win, line, text):
    cursor = 1
    for element in text:
        col = curses.color_pair(element[1])
        if element[2] == "bold":
            col += curses.A_BOLD
        elif element[2] == "italic":
            col += curses.A_ITALIC
        win.addstr(line+1, cursor, element[0], col)
        cursor += len(element[0])
    win.refresh()

def printMultipleText(win, line, listText):
    for i, text in enumerate(listText):
        printText(win, line+i, text)

infoList = [] #list ex: [[("You", 3, "bold"), (" are ", 9, None), ("burning", 4, None), (" for 2 turns", 9, None)]] list of list of tuple that contain a string, a color code and a type
def printInfo(text):
    infoList.append(text) #need to be [("string", color, type of text)]
    infoList.pop(0) if len(infoList) > 6 else None
    for i, text in enumerate(infoList):
        printText(infoWin, 5-i, text)

def printMultipleInfo(listText):
    for text in listText:
        printInfo(text)

if __name__ == "__main__":
    import time
    from classes.Map import Lobby, Room
    from classes.Player import Player

    refreshAll()
    clearMain()
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
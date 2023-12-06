import curses

screen = curses.initscr()
screen.clear()
mainWin = curses.newwin(43, 123, 0, 0) #size 41, 121
mainWin.border()
statsWin = curses.newwin(43, 61, 0, 124) #size 41, 59
statsWin.border()
infoWin = curses.newwin(10, 185, 43, 0) #size 8, 183
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
        # cut the string if it's too long
        t = element[0]
        t = t[:win.getmaxyx()[1]-cursor-1] if len(t) > win.getmaxyx()[1]-cursor-1 else t
        col = curses.color_pair(element[1])
        if element[2] == "bold":
            col += curses.A_BOLD
        elif element[2] == "italic":
            col += curses.A_ITALIC
        win.addstr(line+1, cursor, t, col)
        cursor += len(t)
    win.refresh()

def printMultipleText(win, line, listText):
    for i, text in enumerate(listText):
        printText(win, line+i, text)

infoList = [] #list ex: [[("You", 3, "bold"), (" are ", 9, None), ("burning", 4, None), (" for 2 turns", 9, None)]] list of list of tuple that contain a string, a color code and a type
def printInfo(text):
    infoWin.clear()
    infoWin.border()
    infoList.append(text) #need to be [("string", color, type of text)]
    infoList.pop(0) if len(infoList) > 8 else None
    for i, text in enumerate(infoList):
        printText(infoWin, i, text)

def printMultipleInfo(listText):
    for text in listText:
        printInfo(text)

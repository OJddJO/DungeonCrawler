from keyboard import press
from time import sleep
press('f11') #fullscreen
sleep(0.5)

from classes.Game import MainMenu
if __name__ == "__main__": #execute the game
    game = MainMenu()
    game.run()
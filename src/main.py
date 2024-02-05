from keyboard import press, wait
from time import sleep
press('f11') #fullscreen
sleep(0.5)
print("Press 'f11' if not in fullscreen")
print("Press 'Enter' to continue...")
wait('enter')

from classes.Game import MainMenu
if __name__ == "__main__": #execute the game
    game = MainMenu()
    game.run()
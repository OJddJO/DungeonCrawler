from classes.Game import MainMenu
import gc

gc.enable()
if __name__ == "__main__": #execute the game
    game = MainMenu()
    game.run()
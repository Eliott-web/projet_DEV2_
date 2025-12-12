import threading
from main.game_manager.mini_game.mini_game_utils import getMiniGameList
from main.gui import fenetre
from main.main import setGuiMod

setGuiMod(True)
jeu = getMiniGameList().get("parking")
threading.Timer(0.01, jeu.start).start() # Start
fenetre.start()
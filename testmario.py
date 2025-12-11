from main.gui import fenetre
from main.main import setGuiMod
from main.game_manager.mini_game.mini_game_utils import getMiniGameList
import threading

setGuiMod(True)
jeu = getMiniGameList().get("mario")

threading.Timer(0.01, jeu.start).start() # Start

fenetre.start()
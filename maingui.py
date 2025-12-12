from main.gui import fenetre
from main import main
from main.main import setGuiMod
from main.game_manager.mini_game.mini_game_utils import getMiniGameList
import threading

setGuiMod(True)

threading.Timer(0.01, main.init).start() # Start

fenetre.start()
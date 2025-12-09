from main.gui import fenetre
from main.game_manager.mini_game.mini_game_utils import getMiniGameList

jeu = getMiniGameList().get("mario")
jeu.start()
fenetre.start()
from projet_DEV2_.main.game_manager.mini_game.mini_game_utils import getMiniGameList
from projet_DEV2_.main.gui import fenetre

jeu = getMiniGameList().get("parking")
jeu.start()
fenetre.start()
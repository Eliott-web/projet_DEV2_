from mini_game_utils import getMiniGameList

#mini_game = getMiniGameInstance("Test Game", "A simple test mini-game.")
mini_game = getMiniGameList().get("mario")
mini_game.start()     
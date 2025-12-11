def getMiniGameInstance(name, description):
    from mini_game import MiniGame
    return MiniGame(name, description)

def getMiniGameList():
    from .jeux.mario import MiniGameMario
    from .jeux.garage import MiniGameGarage
    # This function would return a list of available mini-games
    # For simplicity, we return an empty list here
    return {"mario": MiniGameMario(),"parking":MiniGameGarage()}
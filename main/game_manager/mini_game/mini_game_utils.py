from main.game_manager.mini_game.jeux.garage import MiniGameGarage
from main.game_manager.mini_game.jeux.mario import MiniGameMario


game_suppliers = {
    "mario": MiniGameMario,  # Just the class, not an instance
    "parking": MiniGameGarage,
}

def getMiniGameInstance(name: str, description: str):
    return game_suppliers[name](name, description)  # Creates NEW instance

def getMiniGameList():
    return {name: cls() 
            for name, cls in game_suppliers.items()}
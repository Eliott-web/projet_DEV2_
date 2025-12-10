from main.rules.rule import Rule
from main.game_manager.mini_game.controls.control_type_zqsd import ControlTypeZqsd


class toucheInterdite(Rule):

    def __init__(self):
        super().__init__("touche Interdite","si vous appuyez sur la touche interdite, vous perdez 3 points" )

    def on_add(self):

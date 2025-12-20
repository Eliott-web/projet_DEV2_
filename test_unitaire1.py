import unittest
from main.plateau.die import die

# On importe les règles uniquement dans les fonctions pour éviter les circular imports
# et ne pas toucher aux fichiers du groupe

class TestRules(unittest.TestCase):

    # TEST DE LA REGLE DE MAUDIT
    def test_de_maudit(self):
        """
        Spécifications :
        PRE : Le dé fonctionne normalement et permet d’avancer.
        POST : Après activation, chaque lancer fait reculer le joueur.
               Après suppression, le dé redevient normal.
        """
        from main.rules.rules_def.de_maudit import de_mauidit

        rule = de_mauidit()
        rule.on_add()
        self.assertEqual(die.multiplicateur, -1)

        rule.on_remove()
        self.assertEqual(die.multiplicateur, 1)

    # TEST DE LA REGLE MALUS DE
    def test_malus_de(self):
        """
        Spécifications :
        PRE : Le joueur peut avancer avec le dé.
        POST : Après activation, le joueur n’avance plus.
               Après suppression, le joueur peut à nouveau avancer.
        """
        from main.rules.rules_def.malus_de import MalusDe

        rule = MalusDe()
        rule.on_add()
        self.assertEqual(die.multiplicateur, 0)

        rule.on_remove()
        self.assertEqual(die.multiplicateur, 1)

    # TEST DU MINI JEU HARD
    def test_mini_game_hard(self):
        """
        Spécifications :
        PRE : Le mini-jeu dispose d’un temps normal.
        POST : Après activation, le temps du mini-jeu est réduit.
               Après suppression, le temps revient à la valeur initiale.
        """
        from main.rules.rules_def.mini_jeu_hard import MiniGameRule
        from main.game_manager.mini_game.mini_game import MiniGame

        temps_initial = MiniGame.default_time_limit

        rule = MiniGameRule()
        rule.on_add()
        self.assertEqual(MiniGame.default_time_limit, 5)

        rule.on_remove()
        self.assertEqual(MiniGame.default_time_limit, temps_initial)

    # TEST SCORE X2
    def test_score_x2(self):
        """
        Spécifications :
        PRE : Les points sont comptés normalement.
        POST : Après activation, les points sont doublés.
               Après suppression, les points redeviennent normaux.
        """
        from main.rules.rules_def.scorex2 import ScoreX2
        from main.main_loop import plateau_menu

        rule = ScoreX2()
        rule.on_add()
        self.assertEqual(plateau_menu.score_multiplicateur, 2)

        rule.on_remove()
        self.assertEqual(plateau_menu.score_multiplicateur, 1)

    # TEST TURBO TCHIKITA
    def test_turbo(self):
        """
        Spécifications :
        PRE : Le joueur avance normalement.
        POST : Après activation, le joueur avance plus vite.
               Après suppression, le déplacement redevient normal.
        """
        from main.rules.rules_def.turbo_tchikita import Turbo
        from main.main_loop import plateau_menu

        rule = Turbo()
        rule.on_add()
        self.assertEqual(plateau_menu.case_multiplicateur, 2)

        rule.on_remove()
        self.assertEqual(plateau_menu.case_multiplicateur, 1)


if __name__ == "__main__":
    unittest.main()
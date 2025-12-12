"""
Module pour gérer le jeu en mode console
Version texte complète du jeu
"""

import time
from main.console.console_display import ConsoleDisplay
from main.plateau.die.die import lancer_de
from main.rules.rule_list import random_rule_event
import main.main_loop.plateau_menu as plateau_menu_module


class ConsoleGameManager:
    """Gère le jeu en mode console"""
    
    def __init__(self, plateau):
        self.plateau = plateau
        self.pion = plateau.getPion
        self.running = True
        self.score_victoire = 5
        self.score_defaite = -3
    
    def start(self):
        """Démarre le jeu en mode console"""
        ConsoleDisplay.clear()
        ConsoleDisplay.print_header("JEU DE PLATEAU")
        print("\nBienvenue dans le jeu de plateau!")
        ConsoleDisplay.wait_for_key()
        
        while self.running:
            self.game_loop()
        
        # Fin du jeu
        ConsoleDisplay.wait_for_key("Appuyez sur Entrée pour quitter...")
    
    def game_loop(self):
        """Boucle principale du jeu"""
        # Afficher l'état du jeu
        self.display_game_state()
        
        # Menu d'actions
        self.show_main_menu()
    
    def display_game_state(self):
        """Affiche l'état actuel du jeu"""
        ConsoleDisplay.clear()
        
        current_case = self.pion.getCase
        path = self.plateau.getPathArray[0]
        
        # Afficher le plateau
        ConsoleDisplay.print_plateau(self.plateau, current_case)
        
        # Afficher le score et les infos
        inventory_count = len(self.pion.getInventaire)
        ConsoleDisplay.print_score_and_info(
            self.pion.getScore,
            current_case,
            inventory_count
        )
    
    def show_main_menu(self):
        """Affiche le menu principal"""
        case_array = self.plateau.getPathArray[0].getCaseArray
        current_case = case_array[self.pion.getCase]
        
        options = {
            'ESPACE': 'Lancer le dé et avancer',
            'e': 'Ouvrir l\'inventaire',
        }
        
        if current_case.isShop():
            options['i'] = 'Ouvrir la boutique'
        
        options['q'] = 'Quitter'
        
        ConsoleDisplay.print_menu(options)
        
        choice = ConsoleDisplay.input_choice()
        
        if choice == '' or choice == 'espace' or choice == ' ':
            self.lancer_de_et_avancer()
        elif choice == 'e':
            self.open_inventory()
        elif choice == 'i' and current_case.isShop():
            self.open_shop()
        elif choice == 'q':
            self.running = False
    
    def lancer_de_et_avancer(self):
        """Lance le dé et fait avancer le pion"""
        # Lancer le dé
        de = lancer_de()
        
        # Appliquer bonus et multiplicateurs
        bonus = plateau_menu_module.case_bonus
        multiplicateur = plateau_menu_module.case_multiplicateur
        
        total = de * multiplicateur + bonus
        
        # Afficher le résultat
        ConsoleDisplay.print_dice_result(de, bonus, multiplicateur)
        ConsoleDisplay.wait_for_key()
        
        # Réinitialiser le bonus
        plateau_menu_module.case_bonus = 0
        
        # Déplacer le pion
        from main.plateau.plateau_utils import movePion
        movePion(self.plateau, total)
        
        # Vérifier si le jeu est terminé
        path = self.plateau.getPathArray[0]
        if self.pion.getCase >= path.getLength - 1:
            self.end_game(True)
            return
        
        # Lancer un mini-jeu
        ConsoleDisplay.wait_for_key("Appuyez sur Entrée pour lancer le mini-jeu...")
        success = self.play_mini_game_console()
        
        # Appliquer le score
        points = self.score_victoire if success else self.score_defaite
        score_mult = plateau_menu_module.score_multiplicateur
        
        ConsoleDisplay.print_score_change(points, score_mult)
        
        new_score = self.pion.getScore + points * score_mult
        if new_score < 0:
            self.end_game(False)
            return
        
        self.pion.setScore(new_score)
        ConsoleDisplay.wait_for_key()
        
        # Événement de règle
        rule, was_added = random_rule_event()
        if rule is not None:
            ConsoleDisplay.print_rule_event(rule, was_added)
            ConsoleDisplay.wait_for_key()
    
    def play_mini_game_console(self):
        """Joue un mini-jeu en mode console"""
        import random
        
        # Choisir aléatoirement entre le quiz et le jeu de devinette
        game_type = random.choice(['quiz', 'guess'])
        
        if game_type == 'quiz':
            # Mini-jeu Quiz sur le mode GUI
            from main.console.quiz_game import QuizGame
            return QuizGame.play()
        else:
            # Mini-jeu simple : nombre aléatoire
            ConsoleDisplay.print_mini_game_start(
                "Devinez le Nombre",
                "Trouvez le nombre mystère entre 1 et 10!"
            )
            ConsoleDisplay.wait_for_key("Appuyez sur Entrée pour commencer")
            
            target = random.randint(1, 10)
            print(f"\n💭 Quel est le nombre mystère ?")
            
            try:
                guess = int(ConsoleDisplay.input_choice("Votre réponse (1-10): "))
                success = (guess == target)
                
                if success:
                    print(f"✅ Correct! C'était {target}")
                else:
                    print(f"❌ Faux! C'était {target}")
                
                ConsoleDisplay.wait_for_key()
                return success
            except:
                print("❌ Entrée invalide!")
                ConsoleDisplay.wait_for_key()
                return False
    
    def open_inventory(self):
        """Ouvre l'inventaire"""
        inventory = self.pion.getInventaire
        
        if not inventory or len(inventory) == 0:
            ConsoleDisplay.clear()
            print("\n🎒 Inventaire vide!")
            ConsoleDisplay.wait_for_key()
            return
        
        while True:
            ConsoleDisplay.clear()
            ConsoleDisplay.print_inventory(inventory)
            
            print("\n  [Numéro de l'item] Utiliser un item")
            print("  [q] Fermer l'inventaire")
            
            choice = ConsoleDisplay.input_choice()
            
            if choice == 'q':
                break
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(inventory):
                    item = inventory[index]
                    item.onUse()
                    self.pion.removeItem(item)
                    print(f"\n✅ {item.getName()} utilisé!")
                    ConsoleDisplay.wait_for_key()
                    
                    # Rafraîchir l'inventaire
                    inventory = self.pion.getInventaire
                    if not inventory:
                        break
            except:
                print("❌ Choix invalide!")
                ConsoleDisplay.wait_for_key()
    
    def open_shop(self):
        """Ouvre la boutique"""
        from main.item.redbull import RedBull
        from main.item.gomme import Gomme
        
        items = [RedBull(), Gomme()]
        item_price = 3
        
        while True:
            ConsoleDisplay.clear()
            ConsoleDisplay.print_shop(items, self.pion.getScore, None, item_price)
            
            print("\n  [Numéro de l'item] Acheter un item")
            print("  [q] Fermer la boutique")
            
            choice = ConsoleDisplay.input_choice()
            
            if choice == 'q':
                break
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(items):
                    if self.pion.getScore >= item_price:
                        item = items[index]
                        self.pion.addItem(item)
                        self.pion.setScore(self.pion.getScore - item_price)
                        print(f"\n✅ {item.getName()} acheté!")
                        ConsoleDisplay.wait_for_key()
                    else:
                        print("\n❌ Pas assez de points!")
                        ConsoleDisplay.wait_for_key()
            except:
                print("❌ Choix invalide!")
                ConsoleDisplay.wait_for_key()
    
    def end_game(self, reached_end):
        """Termine le jeu"""
        ConsoleDisplay.print_game_end(reached_end)
        print(f"\nScore final: {self.pion.getScore} points")
        self.running = False

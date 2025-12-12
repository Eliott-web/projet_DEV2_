"""
Module pour l'affichage console du jeu
Fournit des fonctions pour afficher proprement le jeu en mode texte
"""

class ConsoleDisplay:
    """Gère l'affichage console du jeu"""
    
    @staticmethod
    def clear():
        """Efface la console"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title):
        """Affiche un en-tête"""
        print("\n" + "=" * 60)
        print(f"  {title.upper()}")
        print("=" * 60)
    
    @staticmethod
    def print_plateau(plateau, current_case):
        """Affiche le plateau de jeu"""
        pion = plateau.getPion
        path = plateau.getPathArray[0]
        length = path.getLength
        
        print("\n📍 PLATEAU DE JEU:")
        print()
        
        # Afficher le chemin avec le pion
        for i in range(length):
            case = path.getCaseArray[i]
            is_current = (i == current_case)
            is_shop = case.isShop()
            
            # Symbole de la case
            if is_shop:
                symbol = "🏪"
            else:
                symbol = "⬜"
            
            # Pion sur la case
            if is_current:
                symbol = "🔵"  # Pion
            
            print(symbol, end=" ")
            
            # Saut de ligne tous les 10 cases
            if (i + 1) % 10 == 0:
                print()
        
        print("\n")
    
    @staticmethod
    def print_score_and_info(score, case_index, inventory_count):
        """Affiche le score et les informations"""
        print(f"\n💰 Score: {score} points")
        print(f"📍 Case: {case_index + 1}")
        print(f"🎒 Items en inventaire: {inventory_count}")
    
    @staticmethod
    def print_menu(options):
        """Affiche un menu avec des options"""
        print("\n" + "-" * 40)
        for key, description in options.items():
            print(f"  [{key}] {description}")
        print("-" * 40)
    
    @staticmethod
    def print_dice_result(value, bonus=0, multiplicateur=1):
        """Affiche le résultat du dé"""
        print(f"\n🎲 Résultat du dé: {value}")
        if multiplicateur > 1:
            print(f"   ×{multiplicateur} (Turbo Tchikita)")
        if bonus > 0:
            print(f"   +{bonus} (Red Bull)")
        total = value * multiplicateur + bonus
        if total != value:
            print(f"   → Total: {total}")
    
    @staticmethod
    def print_score_change(points, multiplicateur=1):
        """Affiche le changement de score"""
        actual_points = points * multiplicateur
        if points > 0:
            print(f"\n✅ +{actual_points} points!")
        else:
            print(f"\n❌ {actual_points} points!")
        
        if multiplicateur > 1:
            print(f"   (×{multiplicateur} Score x2)")
    
    @staticmethod
    def print_rule_event(rule, was_added):
        """Affiche un événement de règle"""
        if was_added:
            print(f"\n✨ NOUVELLE RÈGLE AJOUTÉE!")
        else:
            print(f"\n🗑️  RÈGLE RETIRÉE!")
        
        print(f"   📜 {rule.name}")
        print(f"   {rule.description}")
    
    @staticmethod
    def print_inventory(items, selected_index=None):
        """Affiche l'inventaire"""
        ConsoleDisplay.print_header("INVENTAIRE")
        
        if not items:
            print("\n  Inventaire vide!")
            return
        
        for i, item in enumerate(items):
            marker = "→" if i == selected_index else " "
            print(f"  {marker} [{i+1}] {item.getName()}")
            print(f"       {item.getDescription()}")
    
    @staticmethod
    def print_shop(items, score, selected_index, item_price):
        """Affiche la boutique"""
        ConsoleDisplay.print_header("BOUTIQUE")
        print(f"\n💰 Votre score: {score} points")
        print(f"💵 Prix par item: {item_price} points")
        print()
        
        for i, item in enumerate(items):
            marker = "→" if i == selected_index else " "
            print(f"  {marker} [{i+1}] {item.getName()} - {item_price} pts")
            print(f"       {item.getDescription()}")
    
    @staticmethod
    def print_mini_game_start(name, description):
        """Affiche l'écran de démarrage d'un mini-jeu"""
        ConsoleDisplay.clear()
        ConsoleDisplay.print_header(f"MINI-JEU: {name}")
        print(f"\n{description}")
        print("\n[Appuyez sur ESPACE pour commencer]")
    
    @staticmethod
    def print_mini_game_result(success):
        """Affiche le résultat d'un mini-jeu"""
        if success:
            print("\n✅ GAGNÉ!")
        else:
            print("\n❌ PERDU!")
    
    @staticmethod
    def print_game_end(reached_end):
        """Affiche l'écran de fin de jeu"""
        ConsoleDisplay.clear()
        if reached_end:
            ConsoleDisplay.print_header("FÉLICITATIONS!")
            print("\n🎉 Vous avez gagné!")
        else:
            ConsoleDisplay.print_header("GAME OVER")
            print("\n💀 Vous avez perdu!")
    
    @staticmethod
    def input_choice(prompt="Votre choix: "):
        """Demande une entrée utilisateur"""
        return input(f"\n{prompt}").strip().lower()
    
    @staticmethod
    def wait_for_key(message="Appuyez sur Entrée pour continuer..."):
        """Attend que l'utilisateur appuie sur Entrée"""
        input(f"\n{message}")

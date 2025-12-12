"""
Mini-jeu Quiz pour le mode console
Questions sur les fonctionnalités du mode GUI
"""

import random


class QuizGame:
    """Mini-jeu de quiz sur le mode GUI"""
    
    QUESTIONS = [
        {
            "question": "Le mode GUI a-t-il un moteur physique pour les animations ?",
            "answer": True,
            "explanation": "Oui ! Les cases et le pion utilisent un système d'animation avec vitesse et destination."
        },
        {
            "question": "Peut-on ouvrir un inventaire visuel en appuyant sur 'E' en mode GUI ?",
            "answer": True,
            "explanation": "Oui ! La touche 'E' ouvre un inventaire graphique avec des images d'items."
        },
        {
            "question": "Le mode GUI affiche-t-il les mini-jeux en mode texte uniquement ?",
            "answer": False,
            "explanation": "Faux ! Les mini-jeux sont entièrement graphiques avec Mario Jump et Garage Parking."
        },
        {
            "question": "Les règles s'affichent-elles avec des effets visuels en mode GUI ?",
            "answer": True,
            "explanation": "Oui ! Chaque règle apparaît avec des animations colorées (vert pour ajout, rouge pour retrait)."
        },
        {
            "question": "Y a-t-il une boutique graphique accessible avec 'I' sur certaines cases ?",
            "answer": True,
            "explanation": "Oui ! Les cases 🏪 permettent d'ouvrir une boutique visuelle pour acheter des items."
        },
        {
            "question": "Le score est-il caché en mode GUI ?",
            "answer": False,
            "explanation": "Faux ! Le score est affiché en permanence en haut à droite de l'écran."
        },
        {
            "question": "Les bonus (Red Bull, Turbo) sont-ils affichés visuellement lors du lancer de dé ?",
            "answer": True,
            "explanation": "Oui ! Les multiplicateurs et bonus s'affichent en doré sous le résultat du dé."
        },
        {
            "question": "Le mode GUI n'affiche pas les descriptions des mini-jeux ?",
            "answer": False,
            "explanation": "Faux ! Chaque mini-jeu affiche son nom et sa description en vert/rose sur l'écran de démarrage."
        },
        {
            "question": "Les cases du plateau défilent-elles avec une animation fluide ?",
            "answer": True,
            "explanation": "Oui ! Le plateau défile automatiquement pour suivre le pion avec des animations."
        },
        {
            "question": "Le mode GUI est-il en noir et blanc ?",
            "answer": False,
            "explanation": "Faux ! Le jeu est coloré avec des sprites, des fonds et des effets visuels."
        },
        {
            "question": "Peut-on voir les items de l'inventaire sous forme d'images en mode GUI ?",
            "answer": True,
            "explanation": "Oui ! Chaque item a son propre sprite (Red Bull, Gomme) affiché graphiquement."
        },
        {
            "question": "Les messages de victoire/défaite sont-ils affichés en texte simple en mode GUI ?",
            "answer": False,
            "explanation": "Faux ! Ils apparaissent avec de gros textes colorés et stylisés au centre de l'écran."
        }
    ]
    
    @staticmethod
    def play():
        """Lance le mini-jeu quiz"""
        from main.console.console_display import ConsoleDisplay
        
        ConsoleDisplay.clear()
        ConsoleDisplay.print_header("🎮 QUIZ : Découvrez le Mode GUI !")
        
        print("\n💡 Répondez par 'vrai' ou 'faux' aux questions suivantes")
        print("   pour découvrir les fonctionnalités cachées du mode graphique !")
        print()
        ConsoleDisplay.wait_for_key()
        
        # Sélectionner 3 questions aléatoires
        questions = random.sample(QuizGame.QUESTIONS, 3)
        correct_answers = 0
        
        for i, q in enumerate(questions):
            ConsoleDisplay.clear()
            print(f"\n📝 Question {i+1}/3:")
            print(f"\n   {q['question']}")
            print()
            
            answer = ConsoleDisplay.input_choice("Votre réponse (vrai/faux): ")
            
            # Analyser la réponse
            user_answer = None
            if answer in ['vrai', 'v', 'true', 'yes', 'oui', 'o']:
                user_answer = True
            elif answer in ['faux', 'f', 'false', 'no', 'non', 'n']:
                user_answer = False
            
            # Vérifier la réponse
            if user_answer == q['answer']:
                print("\n✅ CORRECT !")
                correct_answers += 1
            else:
                print("\n❌ FAUX !")
            
            print(f"\n💬 {q['explanation']}")
            ConsoleDisplay.wait_for_key()
        
        # Résultat final
        ConsoleDisplay.clear()
        ConsoleDisplay.print_header("🏆 RÉSULTATS DU QUIZ")
        
        print(f"\n   Score: {correct_answers}/3")
        print()
        
        if correct_answers == 3:
            print("   🌟 PARFAIT ! Vous êtes un expert !")
            print("   Le mode GUI n'a plus de secrets pour vous.")
        elif correct_answers == 2:
            print("   👍 BIEN ! Vous connaissez bien le jeu.")
            print("   Essayez le mode GUI pour en découvrir plus !")
        elif correct_answers == 1:
            print("   🤔 PAS MAL ! Il reste beaucoup à découvrir.")
            print("   Le mode GUI vous réserve de belles surprises !")
        else:
            print("   😅 À REVOIR ! Le mode GUI est fait pour vous !")
            print("   Essayez-le pour découvrir toutes ces fonctionnalités !")
        
        print("\n   💡 Conseil: Lancez le jeu avec guiMode=True dans main.py")
        print("      pour profiter de l'expérience graphique complète !")
        
        ConsoleDisplay.wait_for_key()
        
        # Succès = au moins 2 bonnes réponses
        return correct_answers >= 2

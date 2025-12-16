import random
from main.game_manager.mini_game.entities.mobs.case_entity import CaseEntity
from main.game_manager.mini_game.entities.mobs.pion_entity import PionEntity
from main.game_manager.mini_game.entities.mobs.pion_entity import PionEntity
from main.gui.widget.text import TextWidget
from main.item.gomme import Gomme
from main.item.redbull import RedBull
from main.main_loop.main_menu import MainMenu
from main.game_manager.mini_game.controls.controls_getter import ControlsGetter
from pynput import keyboard
import threading

from main.rules.rule_list import random_rule_event


case_multiplicateur = 1
case_bonus = 0
case_offset = 300
score_multiplicateur = 1
class PlateauMenu(MainMenu, ControlsGetter):

    def __init__(self):
        super().__init__()
        self._current_case_array = []
        self._old_case_index = 0
        self._can_press_key = True
        self.idleText = None
        self.switch_game = False
        self.scoreText = None
        self.inventoryOpen = False
        self.inventoryWidgets = []
        self.inventoryHintText = None
        self.shopHintText = None
        self.selectedInventoryItemIndex = 0
        self.shopOpen = False
        self.shopWidgets = []
        self.selectedItemIndex = 0
        self.ITEM_PRICE = 3

    def build(self):
        self.buildPlateau()
        self.buildPion()
        self.buildScoreDisplay()
        #self.updateCurrentCase()

    def buildPion(self):
        center = self.getCenterXY()
        pion = PionEntity(center)
        self.getMobs().append(pion)
        x = center[0]

        y_ease = 50
        pion.set_position(x ,pion.get_position()[1] + y_ease)
        pion.set_destination_relative(0 ,-y_ease)

    def buildPlateau(self):
        case_array = self.getCaseArray()
        for i in range(len(case_array)):
            case = self.makeCase(i, case_array[i].isShop())
            self.getMobs().append(case)
        

    def makeCase(self, index : int, isShop: bool = False) -> CaseEntity:
        center = self.getCenterXY()
        x = center[0] + (index * case_offset)
        center = (x, center[1] + 60)

        y_ease = 50
        entity = CaseEntity(center, isShop)
        entity.set_position(entity.get_position()[0],entity.get_position()[1] + y_ease)
        entity.set_destination_relative(0,-y_ease)

        proprtional_speed = 1/ (index + 1)
        entity.set_vitesse(entity.get_vitesse() * proprtional_speed)

        self.addToCurrentCaseArray(entity)
        return entity
    
    # Mini jeu

    def lancerMiniGamePre(self):
        self.removeIdleText()
        self.set_can_press_key(False)
        threading.Timer(2, self.lancerMiniGameAnim).start()
    
    def lancerMiniGameAnim(self):
        

        threading.Timer(0.5, self.lancerMiniGamePost).start()
        
    def lancerMiniGamePost(self):
        self.initGamePlay()

    
    def initGamePlay(self):
        from main.game_manager.mini_game.mini_game_utils import getMiniGameList
        self.setPaused(True)
        string = "mario"
        if (self.switch_game):
            string = "parking"
        self.switch_game = not self.switch_game
        jeu = getMiniGameList().get(string)
        jeu.start()


    # Text
    def buildScoreDisplay(self):
        """Crée et affiche le widget de score en haut à droite"""
        from main.gui.fenetre import WIDTH
        score = self.getScore()
        score_text = f"Score: {score}"
        
        # Position en haut à droite (avec une marge de 20 pixels)
        pos_x = WIDTH - 20
        pos_y = 20
        
        self.scoreText = TextWidget(
            score_text,
            font_size=32,
            color=(255, 255, 255),
            pos=(pos_x, pos_y),
            anchor="topright"
        )
        self.ajouterObject(self.scoreText)
    
    def updateScoreDisplay(self):
        """Met à jour l'affichage du score"""
        if self.scoreText:
            score = self.getScore()
            self.scoreText.set_text(f"Score: {score}")
    
    def setIdleText(self):
        from main.gui.fenetre import WIDTH, HEIGHT
        # Afficher le texte au centre en bas de l'écran
        center_x = WIDTH // 2
        center_y = HEIGHT - 200
        text = TextWidget(
            "Appuyez sur 'espace' pour lancer le dé !",
            font_size=36,
            color=(255, 255, 255),
            pos=(center_x, center_y),
            anchor="center"
        )
        self.ajouterObject(text)
        self.idleText = text
        
        # Texte pour ouvrir l'inventaire
        inventory_text = TextWidget(
            "Appuyez sur 'E' pour ouvrir l'inventaire",
            font_size=28,
            color=(200, 200, 200),
            pos=(center_x, center_y + 50),
            anchor="center"
        )
        self.ajouterObject(inventory_text)
        self.inventoryHintText = inventory_text
        
        # Texte pour ouvrir le magasin (seulement si sur une case boutique)
        if self.isOnShop():
            shop_text = TextWidget(
                "Appuyez sur 'I' pour ouvrir le magasin",
                font_size=28,
                color=(255, 215, 0),
                pos=(center_x, center_y + 100),
                anchor="center"
            )
            self.ajouterObject(shop_text)
            self.shopHintText = shop_text


    def removeIdleText(self):
        if self.idleText:
            self.idleText.kill()
            self.idleText = None
        if self.inventoryHintText:
            self.inventoryHintText.kill()
            self.inventoryHintText = None
        if self.shopHintText:
            self.shopHintText.kill()
            self.shopHintText = None

    def setDiceText(self, text, bonus=0, multiplicateur=1):
        from main.gui.fenetre import WIDTH, HEIGHT
        # Afficher le texte au centre en bas de l'écran
        center_x = WIDTH // 2
        center_y = 300
        dice_text = TextWidget(
            text,
            font_size=100,
            color=(255, 255, 255),
            pos=(center_x, center_y),
            anchor="center"
        )
        self.ajouterObject(dice_text)
        threading.Timer(2, dice_text.kill).start()
        
        # Afficher les bonus/multiplicateurs si actifs
        bonus_messages = []
        if multiplicateur > 1:
            bonus_messages.append(f"×{multiplicateur} (Turbo Tchikita)")
        if bonus > 0:
            bonus_messages.append(f"+{bonus} (Red Bull)")
        
        if bonus_messages:
            bonus_text = TextWidget(
                " | ".join(bonus_messages),
                font_size=36,
                color=(255, 215, 0),
                pos=(center_x, center_y + 80),
                anchor="center",
                bold=True
            )
            self.ajouterObject(bonus_text)
            threading.Timer(2, bonus_text.kill).start()

    def setScoreChangeText(self, points):
        """Affiche un gros message temporaire pour annoncer le gain ou la perte de points"""
        global score_multiplicateur
        from main.gui.fenetre import WIDTH, HEIGHT
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        
        # Définir le texte et la couleur selon le gain ou la perte
        if points > 0:
            text = f"+{points} points !"
            color = (0, 255, 0)  # Vert pour un gain
        elif points < 0:
            text = f"{points} points !"
            color = (255, 0, 0)  # Rouge pour une perte
        else:
            text = "0 point"
            color = (255, 255, 255)  # Blanc pour zéro
        
        score_text = TextWidget(
            text,
            font_size=120,
            color=color,
            pos=(center_x, center_y),
            anchor="center",
            bold=False
        )
        self.ajouterObject(score_text)
        threading.Timer(2.5, score_text.kill).start()
        
        # Afficher le multiplicateur si actif
        if score_multiplicateur > 1:
            multiplier_text = TextWidget(
                f"×{score_multiplicateur} (Score x2)",
                font_size=48,
                color=(255, 215, 0),
                pos=(center_x, center_y + 100),
                anchor="center",
                bold=True
            )
            self.ajouterObject(multiplier_text)
            threading.Timer(2.5, multiplier_text.kill).start()

    # Menu d'inventaire
    def toggleInventory(self):
        """Ouvre ou ferme le menu d'inventaire"""
        if self.inventoryOpen:
            self.closeInventory()
        else:
            self.openInventory()
    
    def openInventory(self):
        """Ouvre le menu d'inventaire"""
        if self.inventoryOpen:
            return
        
        # Vérifier si l'inventaire est vide
        inventory = self.getInventory()
        if not inventory or len(inventory) == 0:
            self.showEmptyInventoryMessage()
            return
        
        from main.gui.fenetre import WIDTH, HEIGHT
        from main.gui.widget.image import ImageWidget
        
        self.inventoryOpen = True
        self.selectedInventoryItemIndex = 0
        
        # Fond semi-transparent
        overlay_bg = ImageWidget(
            "assets/gui/logo.png",
            pos=(WIDTH // 2, HEIGHT // 2),
            size=(WIDTH, HEIGHT),
            anchor="center",
            alpha=150
        )
        self.inventoryWidgets.append(overlay_bg)
        
        # Titre de l'inventaire
        title = TextWidget(
            "INVENTAIRE",
            font_size=48,
            color=(255, 255, 255),
            pos=(WIDTH // 2, 50),
            anchor="center",
            bold=True
        )
        self.inventoryWidgets.append(title)
        
        # Instructions
        instructions = TextWidget(
            "Utilisez les FLÈCHES pour naviguer | ESPACE pour utiliser | 'E' pour fermer",
            font_size=22,
            color=(200, 200, 200),
            pos=(WIDTH // 2, 100),
            anchor="center"
        )
        self.inventoryWidgets.append(instructions)
        
        # Afficher les items
        self.displayInventoryItems()
    
    def displayInventoryItems(self):
        """Affiche les items de l'inventaire"""
        from main.gui.fenetre import WIDTH, HEIGHT
        from main.gui.widget.image import ImageWidget
        
        inventory_items = self.getInventory()
        
        if not inventory_items:
            return
        
        item_size = 100
        spacing = 150
        # Calculer dynamiquement la position de départ selon le nombre d'items
        start_x = WIDTH // 2 - (spacing * (len(inventory_items) - 1)) // 2
        start_y = HEIGHT // 2 - 20
        
        for i, item in enumerate(inventory_items):
            x = start_x + (i * spacing)
            y = start_y
            
            # Déterminer si c'est l'item sélectionné
            is_selected = (i == self.selectedInventoryItemIndex)
            
            # Cadre de sélection
            if is_selected:
                selection_box = TextWidget(
                    "▼ SÉLECTIONNÉ ▼",
                    font_size=20,
                    color=(100, 255, 100),
                    pos=(x, y - 70),
                    anchor="center",
                    bold=True
                )
                self.inventoryWidgets.append(selection_box)
            
            # Image de l'item
            item_widget = ImageWidget(
                item.getImagePath(),
                pos=(x, y),
                size=(item_size, item_size),
                anchor="center",
                alpha=255
            )
            self.inventoryWidgets.append(item_widget)
            
            # Nom de l'item
            item_name = TextWidget(
                item.getName(),
                font_size=24,
                color=(255, 255, 255) if is_selected else (180, 180, 180),
                pos=(x, y + item_size // 2 + 25),
                anchor="center",
                bold=is_selected
            )
            self.inventoryWidgets.append(item_name)
        
        # Afficher la description de l'item sélectionné
        if 0 <= self.selectedInventoryItemIndex < len(inventory_items):
            selected_item = inventory_items[self.selectedInventoryItemIndex]
            description = TextWidget(
                selected_item.getDescription(),
                font_size=28,
                color=(220, 220, 220),
                pos=(WIDTH // 2, HEIGHT - 300),
                anchor="center"
            )
            self.inventoryWidgets.append(description)
    
    def closeInventory(self):
        """Ferme le menu d'inventaire"""
        if not self.inventoryOpen:
            return
        
        self.inventoryOpen = False
        self.selectedInventoryItemIndex = 0
        
        # Supprimer tous les widgets de l'inventaire
        for widget in self.inventoryWidgets:
            try:
                widget.kill()
            except:
                pass
        self.inventoryWidgets.clear()
    
    def navigateInventory(self, direction):
        """Navigue dans les items de l'inventaire"""
        if not self.inventoryOpen:
            return
        
        inventory_items = self.getInventory()
        if not inventory_items:
            return
        
        # Mettre à jour l'index sélectionné
        if direction == "left":
            self.selectedInventoryItemIndex = (self.selectedInventoryItemIndex - 1) % len(inventory_items)
        elif direction == "right":
            self.selectedInventoryItemIndex = (self.selectedInventoryItemIndex + 1) % len(inventory_items)
        
        # Rafraîchir l'affichage
        self.refreshInventoryDisplay()
    
    def refreshInventoryDisplay(self):
        """Rafraîchit l'affichage de l'inventaire"""
        # Supprimer les anciens widgets (sauf le fond, titre et instructions)
        widgets_to_keep = self.inventoryWidgets[:3]  # Garder overlay, titre, instructions
        
        for widget in self.inventoryWidgets[3:]:
            try:
                widget.kill()
            except:
                pass
        
        self.inventoryWidgets = widgets_to_keep
        
        # Réafficher les items
        self.displayInventoryItems()
    
    def useSelectedItem(self):
        """Utilise l'item sélectionné"""
        if not self.inventoryOpen:
            return
        
        inventory_items = self.getInventory()
        if not inventory_items or self.selectedInventoryItemIndex >= len(inventory_items):
            return
        
        # Récupérer l'item sélectionné
        selected_item = inventory_items[self.selectedInventoryItemIndex]
        pion = self.getPlateau().getPion
        
        # Utiliser l'item
        selected_item.onUse()
        
        # Retirer l'item de l'inventaire
        pion.removeItem(selected_item)
        
        # Afficher un message de confirmation
        self.showItemUsedMessage(selected_item.getName())
        
        # Vérifier si l'inventaire est maintenant vide
        if len(self.getInventory()) == 0:
            self.closeInventory()
            return
        
        # Ajuster l'index si nécessaire
        if self.selectedInventoryItemIndex >= len(self.getInventory()):
            self.selectedInventoryItemIndex = len(self.getInventory()) - 1
        
        # Rafraîchir l'affichage
        self.refreshInventoryDisplay()
    
    def showItemUsedMessage(self, item_name):
        """Affiche un message indiquant qu'un item a été utilisé"""
        from main.gui.fenetre import WIDTH, HEIGHT
        
        message = TextWidget(
            f"Utilisé: {item_name} !",
            font_size=54,
            color=(100, 200, 255),
            pos=(WIDTH // 2, HEIGHT // 2 - 150),
            anchor="center",
            bold=True
        )
        self.ajouterObject(message)
        threading.Timer(2, message.kill).start()

    def showEmptyInventoryMessage(self):
        """Affiche un message indiquant que l'inventaire est vide"""
        from main.gui.fenetre import WIDTH, HEIGHT
        
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        
        message = TextWidget(
            "Inventaire vide !",
            font_size=60,
            color=(255, 100, 100),
            pos=(center_x, center_y),
            anchor="center",
            bold=True
        )
        self.ajouterObject(message)
        threading.Timer(2, message.kill).start()

    # Menu de boutique
    def toggleShop(self):
        """Ouvre ou ferme la boutique"""
        if self.shopOpen:
            self.closeShop()
        else:
            self.openShop()
    
    def openShop(self):
        """Ouvre le menu de la boutique"""
        if self.shopOpen:
            return
        
        # Vérifier si on est sur une case boutique
        if not self.isOnShop():
            self.showNotOnShopMessage()
            return
        
        from main.gui.fenetre import WIDTH, HEIGHT
        from main.gui.widget.image import ImageWidget
        
        self.shopOpen = True
        self.selectedItemIndex = 0
        
        # Fond semi-transparent
        overlay_bg = ImageWidget(
            "assets/background/shop.png",
            pos=(WIDTH // 2, HEIGHT // 2),
            size=(WIDTH, int(HEIGHT * 1.1)),
            anchor="center",
            alpha=255
        )
        self.shopWidgets.append(overlay_bg)
        
        # Titre de la boutique
        title = TextWidget(
            "BOUTIQUE",
            font_size=48,
            color=(255, 215, 0),
            pos=(WIDTH // 2, 50),
            anchor="center",
            bold=True
        )
        self.shopWidgets.append(title)
        
        # Instructions
        instructions = TextWidget(
            "Utilisez les FLÈCHES pour naviguer | ESPACE pour acheter | 'I' pour fermer",
            font_size=22,
            color=(0, 0, 0),
            pos=(WIDTH // 2, 100),
            anchor="center"
        )
        self.shopWidgets.append(instructions)
        
        # Afficher le score actuel
        score_display = TextWidget(
            f"Votre score: {self.getScore()} points",
            font_size=28,
            color=(100, 255, 100),
            pos=(WIDTH // 2, 140),
            anchor="center",
            bold=True
        )
        self.shopWidgets.append(score_display)
        
        # Afficher les items
        self.displayShopItems()
    
    def displayShopItems(self):
        """Affiche les items de la boutique"""
        from main.gui.fenetre import WIDTH, HEIGHT
        from main.gui.widget.image import ImageWidget
        
        buyable_items = self.getBuyableItems()
        
        if not buyable_items:
            no_items = TextWidget(
                "Aucun item disponible",
                font_size=36,
                color=(0, 0, 0),
                pos=(WIDTH // 2, HEIGHT // 2),
                anchor="center"
            )
            self.shopWidgets.append(no_items)
            return
        
        item_size = 100
        spacing = 150
        start_x = WIDTH // 2 - (spacing * (len(buyable_items) - 1)) // 2
        start_y = HEIGHT // 2 - 20
        
        for i, item in enumerate(buyable_items):
            x = start_x + (i * spacing)
            y = start_y
            
            # Déterminer si c'est l'item sélectionné
            is_selected = (i == self.selectedItemIndex)
            
            # Cadre de sélection
            if is_selected:
                selection_box = TextWidget(
                    "▼ SÉLECTIONNÉ ▼",
                    font_size=20,
                    color=(255, 215, 0),
                    pos=(x, y - 70),
                    anchor="center",
                    bold=True
                )
                self.shopWidgets.append(selection_box)
            
            # Image de l'item
            item_widget = ImageWidget(
                item.getImagePath(),
                pos=(x, y),
                size=(item_size, item_size),
                anchor="center",
                alpha=255
            )
            self.shopWidgets.append(item_widget)
            
            # Nom de l'item
            item_name = TextWidget(
                item.getName(),
                font_size=24,
                color=(255, 255, 255) if is_selected else (0, 0, 0),
                pos=(x, y + item_size // 2 + 25),
                anchor="center",
                bold=is_selected
            )
            self.shopWidgets.append(item_name)
            
            # Prix
            price_text = TextWidget(
                f"{self.ITEM_PRICE} points",
                font_size=20,
                color=(100, 255, 100) if is_selected else (100, 200, 100),
                pos=(x, y + item_size // 2 + 55),
                anchor="center",
                bold=is_selected
            )
            self.shopWidgets.append(price_text)
        
        # Afficher la description de l'item sélectionné
        if 0 <= self.selectedItemIndex < len(buyable_items):
            selected_item = buyable_items[self.selectedItemIndex]
            description = TextWidget(
                selected_item.getDescription(),
                font_size=32,
                color=(0, 0, 0),
                pos=(WIDTH // 2, HEIGHT - 100),
                anchor="center"
            )
            self.shopWidgets.append(description)
    
    def closeShop(self):
        """Ferme le menu de la boutique"""
        if not self.shopOpen:
            return
        
        self.shopOpen = False
        self.selectedItemIndex = 0
        
        # Supprimer tous les widgets de la boutique
        for widget in self.shopWidgets:
            try:
                widget.kill()
            except:
                pass
        self.shopWidgets.clear()
    
    def navigateShop(self, direction):
        """Navigue dans les items de la boutique"""
        if not self.shopOpen:
            return
        
        buyable_items = self.getBuyableItems()
        if not buyable_items:
            return
        
        # Mettre à jour l'index sélectionné
        if direction == "left":
            self.selectedItemIndex = (self.selectedItemIndex - 1) % len(buyable_items)
        elif direction == "right":
            self.selectedItemIndex = (self.selectedItemIndex + 1) % len(buyable_items)
        
        # Rafraîchir l'affichage
        self.refreshShopDisplay()
    
    def refreshShopDisplay(self):
        """Rafraîchit l'affichage de la boutique"""
        # Supprimer les anciens widgets (sauf le fond et les titres)
        widgets_to_keep = self.shopWidgets[:4]  # Garder overlay, titre, instructions, score
        
        for widget in self.shopWidgets[4:]:
            try:
                widget.kill()
            except:
                pass
        
        self.shopWidgets = widgets_to_keep
        
        # Mettre à jour le score
        if len(self.shopWidgets) >= 4:
            try:
                self.shopWidgets[3].kill()
            except:
                pass
            
            from main.gui.fenetre import WIDTH
            score_display = TextWidget(
                f"Votre score: {self.getScore()} points",
                font_size=28,
                color=(100, 255, 100),
                pos=(WIDTH // 2, 140),
                anchor="center",
                bold=True
            )
            self.shopWidgets[3] = score_display
        
        # Réafficher les items
        self.displayShopItems()
    
    def buySelectedItem(self):
        """Achète l'item sélectionné"""
        if not self.shopOpen:
            return
        
        buyable_items = self.getBuyableItems()
        if not buyable_items or self.selectedItemIndex >= len(buyable_items):
            return
        
        current_score = self.getScore()
        
        # Vérifier si le joueur a assez de points ET que le score ne sera pas <= 0 après l'achat
        if current_score < self.ITEM_PRICE or (current_score - self.ITEM_PRICE) <= 0:
            self.showInsufficientFundsMessage()
            return
        
        # Acheter l'item
        selected_item = buyable_items[self.selectedItemIndex]
        pion = self.getPlateau().getPion
        
        # Ajouter l'item à l'inventaire
        pion.addItem(selected_item)
        
        # Déduire le prix
        self.addScore(-self.ITEM_PRICE)
        
        self.showPurchaseSuccessMessage(selected_item.getName())
        
        # Rafraîchir l'affichage
        self.refreshShopDisplay()
    
    def showNotOnShopMessage(self):
        """Affiche un message indiquant qu'on n'est pas sur une boutique"""
        from main.gui.fenetre import WIDTH, HEIGHT
        
        message = TextWidget(
            "Vous n'êtes pas sur une case boutique !",
            font_size=48,
            color=(255, 100, 100),
            pos=(WIDTH // 2, HEIGHT // 2),
            anchor="center",
            bold=True
        )
        self.ajouterObject(message)
        threading.Timer(2, message.kill).start()
    
    def showInsufficientFundsMessage(self):
        """Affiche un message indiquant un manque de points"""
        from main.gui.fenetre import WIDTH, HEIGHT
        
        message = TextWidget(
            "Pas assez de points !",
            font_size=54,
            color=(255, 50, 50),
            pos=(WIDTH // 2, HEIGHT // 2 - 150),
            anchor="center",
            bold=True
        )
        self.ajouterObject(message)
        threading.Timer(2, message.kill).start()
    
    def showPurchaseSuccessMessage(self, item_name):
        """Affiche un message de succès d'achat"""
        from main.gui.fenetre import WIDTH, HEIGHT
        
        message = TextWidget(
            f"Acheté: {item_name} !",
            font_size=54,
            color=(100, 255, 100),
            pos=(WIDTH // 2, HEIGHT // 2 - 150),
            anchor="center",
            bold=True
        )
        self.ajouterObject(message)
        threading.Timer(2, message.kill).start()
    
    def showShopNotification(self):
        """Affiche un message en haut à gauche pour informer qu'on est sur une case magasin"""
        message = TextWidget(
            "Case Magasin - Appuyez sur 'I' pour acheter",
            font_size=28,
            color=(255, 215, 0),  # Couleur or
            pos=(20, 20),
            anchor="topleft",
            bold=True
        )
        self.ajouterObject(message)
        threading.Timer(4, message.kill).start()

    # Gestion des règles
    def ruleEvents(self):
        """Applique un événement de règle aléatoire et affiche le résultat
        
        Returns:
            tuple: (Rule, bool) - La règle et si elle a été ajoutée (True) ou retirée (False)
                   ou (None, None) si aucune action
        """
        from main.rules.rule_list import random_rule_event
        from main.gui.fenetre import WIDTH, HEIGHT
        
        rule, was_added = random_rule_event()
        
        if rule is None:
            return (None, None)
        
        # Déterminer le message et la couleur
        if was_added:
            action_text = "NOUVELLE RÈGLE AJOUTÉE !"
            color = (100, 255, 100)  # Vert
        else:
            action_text = "RÈGLE RETIRÉE !"
            color = (255, 100, 100)  # Rouge
        
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        
        # Titre de l'action (ajoutée ou retirée)
        title = TextWidget(
            action_text,
            font_size=48,
            color=color,
            pos=(center_x, center_y - 100),
            anchor="center",
            bold=True
        )
        self.ajouterObject(title)
        
        # Nom de la règle
        rule_name = TextWidget(
            rule.name,
            font_size=42,
            color=(255, 255, 255),
            pos=(center_x, center_y - 20),
            anchor="center",
            bold=True
        )
        self.ajouterObject(rule_name)
        
        # Description de la règle
        rule_description = TextWidget(
            rule.description,
            font_size=28,
            color=(220, 220, 220),
            pos=(center_x, center_y + 40),
            anchor="center"
        )
        self.ajouterObject(rule_description)
        
        # Faire disparaître les widgets après 3.5 secondes
        threading.Timer(3.5, title.kill).start()
        threading.Timer(3.5, rule_name.kill).start()
        threading.Timer(3.5, rule_description.kill).start()
        
        return (rule, was_added)
    
    def displayRemovedRule(self, rule):
        """Affiche une règle qui vient d'être retirée
        
        Args:
            rule: La règle retirée à afficher
        """
        if rule is None:
            return
        
        from main.gui.fenetre import WIDTH, HEIGHT
        
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        
        # Titre de l'action
        title = TextWidget(
            "RÈGLE RETIRÉE !",
            font_size=48,
            color=(255, 100, 100),  # Rouge
            pos=(center_x, center_y - 100),
            anchor="center",
            bold=True
        )
        self.ajouterObject(title)
        
        # Nom de la règle
        rule_name = TextWidget(
            rule.name,
            font_size=42,
            color=(255, 255, 255),
            pos=(center_x, center_y - 20),
            anchor="center",
            bold=True
        )
        self.ajouterObject(rule_name)
        
        # Description de la règle
        rule_description = TextWidget(
            rule.description,
            font_size=28,
            color=(220, 220, 220),
            pos=(center_x, center_y + 40),
            anchor="center"
        )
        self.ajouterObject(rule_description)
        
        # Faire disparaître les widgets après 3.5 secondes
        threading.Timer(3.5, title.kill).start()
        threading.Timer(3.5, rule_name.kill).start()
        threading.Timer(3.5, rule_description.kill).start()


    def miniGameEnded(self, success: bool):
        self.setPaused(False)
        self.set_can_press_key(False)  # Désactiver les contrôles pendant l'affichage
        scoreVictoire = 5
        scoreDefaite = -3

        # Afficher le score d'abord
        if success:
            self.addScore(scoreVictoire)
        else:
            self.addScore(scoreDefaite)
        
        # Fonction pour afficher la règle après le score
        def show_rule():
            rule, was_added = self.ruleEvents()
            
            # Afficher le message de magasin si on est sur une case boutique
            if self.isOnShop():
                self.showShopNotification()
            
            # Réactiver les contrôles après l'affichage de la règle (3.5s de durée)
            if rule is not None:
                threading.Timer(3.5, lambda: self.set_can_press_key(True)).start()
            else:
                # Si pas de règle, réactiver immédiatement
                self.set_can_press_key(True)
        
        # Attendre 2.5 secondes (durée du message de score) avant d'afficher la règle
        threading.Timer(2.5, show_rule).start()

    # Actions du joueur

    def initEnd(self, reached_end=True):
        self.setPaused(True)
        self.set_can_press_key(False)
        
        from main.gui.fenetre import WIDTH, HEIGHT
        import sys
        
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        
        if reached_end:
            text = "FÉLICITATIONS ! Vous avez gagné !"
            color = (100, 255, 100)  # Vert
            pass
        else:
            text = "GAME OVER Vous avez perdu !"
            color = (255, 100, 100)  # Rouge
            pass
        
        end_message = TextWidget(
            text,
            font_size=72,
            color=color,
            pos=(center_x, center_y),
            anchor="center",
            bold=True
        )
        self.ajouterObject(end_message)
        
        # Fermer le jeu après 3 secondes
        def quit_game():
            pass
            sys.exit(0)
        
        threading.Timer(3, quit_game).start()

    def moveAll(self):
        plateau = self.getPlateau()
        pion = plateau.getPion
        path = plateau.getPathArray[pion.getPath]
        if pion.getCase >= path.getLength - 1:
            self.initEnd(True)
            return
        self.avancerPion()
        self.updateCurrentCase()

    def jetDe(self):
        global case_bonus, case_multiplicateur
        from main.plateau.die.die import lancer_de
        value = lancer_de()
        string = f"Tu as obtenu : {value} !"
        self.setDiceText(string, case_bonus, case_multiplicateur)
        return value
    
    def avancerPion(self):
        global case_bonus, case_multiplicateur
        from main.plateau.plateau_utils import movePion

        de = self.jetDe()

        de += case_bonus
        de *= case_multiplicateur
        case_bonus = 0
        
        movePion(self.getPlateau(), de)
        self.updateScoreDisplay()
        
        # Vérifier si le pion a atteint la fin
        plateau = self.getPlateau()
        pion = plateau.getPion
        path = plateau.getPathArray[pion.getPath]
        if pion.getCase >= path.getLength - 1:
            # Désactiver les contrôles immédiatement
            self.set_can_press_key(False)
            # Attendre 2 secondes pour laisser l'animation du pion se terminer
            threading.Timer(2, lambda: self.initEnd(True)).start()
        else:
            self.lancerMiniGamePre()

    def updateCurrentCase(self):
        currentCase = self.getCurrentCaseIndex()
        for case in self.getCurrentCaseArray():
            case.set_destination_relative(-case_offset * (currentCase - self.getOldCaseIndex()), 0)
            case.set_vitesse(80)
        self.setOldCaseIndex(currentCase)

    def addToCurrentCaseArray(self, case):
        self._current_case_array.append(case)

    def getCurrentCaseArray(self):
        return self._current_case_array

    def getCurrentCaseIndex(self):
        pion = self.getPlateau().getPion
        return pion.getCase

    def getCurrentCase(self):
        index = self.getCurrentCaseIndex()
        case_array = self.getCurrentCaseArray()
        if 0 <= index < len(case_array):
            return case_array[index]
        return None
    
    def getScore(self):
        pion = self.getPlateau().getPion
        return pion.getScore
    
    def getInventory(self):
        pion = self.getPlateau().getPion
        return pion.getInventaire

    def addScore(self, points):
        global score_multiplicateur

        pion = self.getPlateau().getPion
        new_score = pion.getScore + points * score_multiplicateur
        if new_score < 0:
            self.initEnd(False)
            return
        pion.setScore(new_score)
        self.updateScoreDisplay()
        self.setScoreChangeText(points)

    def getOldCaseIndex(self):
        return self._old_case_index
    
    def setOldCaseIndex(self, index):
        self._old_case_index = index

    def getCaseArray(self):
        plateau = self.getPlateau()
        paths = plateau.getPathArray
        if paths:
            path = paths[0]
            return path.getCaseArray
        return []
    
    def isOnShop(self):
        current_case = self.getCurrentCase()
        if current_case:
            return current_case.isShop()
        return False
    
    def getBuyableItems(self):
        items = [RedBull(),Gomme()]
        return items



    def space_on_press(self):
        # Si l'inventaire est ouvert, utiliser l'item
        if self.inventoryOpen:
            self.useSelectedItem()
            return None
        
        # Si la boutique est ouverte, acheter l'item
        if self.shopOpen:
            self.buySelectedItem()
            return None
        
        self.moveAll()
        """Placeholder invoked when the Space key is pressed."""
        return None

    def e_on_press(self):
        """Ouvre ou ferme l'inventaire quand 'E' est pressé."""
        self.toggleInventory()
        return None
    
    def i_on_press(self):
        """Ouvre ou ferme la boutique quand 'I' est pressé."""
        self.toggleShop()
        return None


    def on_press(self, key):
        if (self.isPaused() or not self.get_can_press_key()):
            return
        
        if key == keyboard.Key.space:
            self.space_on_press()
        elif hasattr(key, 'char') and key.char == 'e':
            self.e_on_press()
        elif hasattr(key, 'char') and key.char == 'i':
            self.i_on_press()
        elif key == keyboard.Key.left:
            if self.shopOpen:
                self.navigateShop("left")
            elif self.inventoryOpen:
                self.navigateInventory("left")
        elif key == keyboard.Key.right:
            if self.shopOpen:
                self.navigateShop("right")
            elif self.inventoryOpen:
                self.navigateInventory("right")

    def get_can_press_key(self):
        return self._can_press_key
    
    def set_can_press_key(self, can_press):
        self._can_press_key = can_press
    
    def start(self):
        self.build()
        super().start()

    def loop_start(self):
        self.setIdleText()
        super().loop_start()

    def loop(self):
        self.checkControls()
        super().loop()

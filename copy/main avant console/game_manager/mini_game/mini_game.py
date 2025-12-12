import time
import threading

from main.game_manager.mini_game.controls.control_type_space import ControlTypeSpace
from main.gui.fenetre import HEIGHT, WIDTH
from main.gui.widget.image import ImageWidget
from .controls.controls_getter import ControlsGetter

class MiniGame(ControlsGetter):
    default_time_limit = 5  # secondes
    refresh_rate = 20  # FPS

    def __init__(self, name, description):
        self._name = name
        self._description = description
        self._time_limit = MiniGame.default_time_limit
        self._timer = 0
        self._mobs = []
        self._objects = []
        self._hasStarted = False
        self._endInstantly = False
        self._start_control = None
        self._cleanup_timer = None
        self._text_space = None
        self._text_end = None
        self._loop_timer = None  # Track the loop timer to cancel it

    def __repr__(self):
        return f"Mini-jeu: {self._name} - {self._description}"

    # Public API
    def afficherStartText(self):
        from main.gui.widget.text import TextWidget
        
        # Image de fond
        self._text_space = ImageWidget("assets/gui/start.png", self.getCenterXY(), (1536/2,1024/2), 
            anchor="center", on_click=lambda w: None)
        
        # Texte avec le nom du mini-jeu
        center_x, center_y = self.getCenterXY()
        self._game_title = TextWidget(
            self._name,
            font_size=64,
            color=(255, 255, 255),
            pos=(center_x, 100),
            anchor="center",
            bold=True
        )
        
        # Description du mini-jeu
        self._game_description = TextWidget(
            self._description,
            font_size=36,
            color=(255, 20, 147),  # Rose foncé
            pos=(center_x, 150),
            anchor="center"
        )

    def stopStartText(self):
        if self._text_space:
            self._text_space.kill()
            self._text_space = None
        if hasattr(self, '_game_title') and self._game_title:
            self._game_title.kill()
            self._game_title = None
        if hasattr(self, '_game_description') and self._game_description:
            self._game_description.kill()
            self._game_description = None

    def afficherEndText(self, win):
        image = None
        if win:
            image =    ImageWidget("assets/gui/win.png", self.getCenterXY(), (1536/2,1024/2), 
            anchor="center", on_click=lambda w: None)
        else:
            image = ImageWidget("assets/gui/perdu.png", self.getCenterXY(), (1536/2,1024/2), 
            anchor="center", on_click=lambda w: None)
        self._text_end = image

    def stopEndText(self):
        if self._text_end:
            self._text_end.kill()
            self._text_end = None

    def start(self):
        """Load/init everything but don't run the main loop until Space is pressed."""
        print(f"Démarrage du mini-jeu (chargement): {self._name}")
        self.load()
        self.setup_start_listener()
        print("Appuyez sur Espace pour démarrer le mini-jeu...")
        self.afficherStartText()

    def endInstantly(self, win: bool): # Si tu veux que ça se termine tout de suite victoire/défaite
        self._endInstantly = True
        self._schedule_final_cleanup(win, delay=2.0)

    # -- Loading / start handling (separated) --
    def load(self):
        """Prepare the mini-game state (reset timer, keep mobs/objects ready)."""
        self.reset_timer()
        self._hasStarted = False
        self._endInstantly = False

    def setup_start_listener(self):
        """Listen for the Space key and begin the game when pressed."""
        self._start_control = ControlTypeSpace()
        def _bound_space():
            self._on_space_pressed()
        self._start_control.space_pressed = _bound_space
        self._start_control.checkControls()

    def _on_space_pressed(self):
        """Internal handler called when Space is pressed to start the loop."""
        if self._hasStarted:
            return
        # stop the temporary start listener if possible
        try:
            if self._start_control and hasattr(self._start_control, '_listener'):
                self._start_control._listener.stop()
        except Exception:
            pass
        self.stopStartText()
        self.begin_loop()

    def begin_loop(self):
        """Set started flag, reset timer and start the main loop."""
        # Cancel any existing loop timer from previous game
        if self._loop_timer:
            self._loop_timer.cancel()
            self._loop_timer = None
        self._hasStarted = True
        self.reset_timer()
        self.loop()

    # -- End / cleanup handling (separated) --
    def end(self, success):
        """
        Called to end the mini-game. Stops gameplay immediately and schedules
        the real cleanup 2 seconds later to 'deload' resources.
        """
        self._initiate_end(success)

    def _initiate_end(self, success):
        """Stop gameplay and listeners immediately, then schedule cleanup."""
        # Cancel the loop timer to stop the game loop
        if self._loop_timer:
            self._loop_timer.cancel()
            self._loop_timer = None
        
        # prevent further game activity
        self._endInstantly = True
        self._hasStarted = False

        # stop any in-game controls listener on this instance
        try:
            if hasattr(self, '_listener'):
                self._listener.stop()
        except Exception:
            pass

        # stop the start listener if it's still present
        try:
            if self._start_control and hasattr(self._start_control, '_listener'):
                self._start_control._listener.stop()
        except Exception:
            pass

        # schedule final cleanup after 2 seconds (or replace delay as needed)
        self._schedule_final_cleanup(success, delay=2.0)

        # immediate feedback
        print(f"Mini-jeu: {self._name} — arrêt demandé, nettoyage dans 2s...")

    def _schedule_final_cleanup(self, success, delay=2.0):
        self.afficherEndText(success)
        """Schedule (or run immediately if delay == 0) the final cleanup."""
        # cancel any previously scheduled cleanup
        try:
            if self._cleanup_timer and isinstance(self._cleanup_timer, threading.Timer):
                self._cleanup_timer.cancel()
        except Exception:
            pass

        if delay <= 0.0:
            self._finalize_end(success)
        else:
            self._cleanup_timer = threading.Timer(delay, self._finalize_end, args=(success,))
            self._cleanup_timer.start()

    def _finalize_end(self, success):
        """Kill/deload mobs and objects and print final result."""
        from main import main
        menu = main.mainMenu
        menu.setPaused(False)
        menu.set_can_press_key(True)
        menu.miniGameEnded(success)


        self.stopEndText()
        # kill mobs and clear
    
        for mob in list(self._mobs):
            try:
                mob.kill()
            except Exception:
                pass
        self._mobs.clear()

        # kill objects and clear
        for obj in list(self._objects):
            try:
                obj.kill()
            except Exception:
                pass
        self._objects.clear()

        # ensure listeners are stopped
        try:
            if hasattr(self, '_listener'):
                self._listener.stop()
        except Exception:
            pass

        try:
            if self._start_control and hasattr(self._start_control, '_listener'):
                self._start_control._listener.stop()
        except Exception:
            pass

        # finalize state
        self._hasStarted = False
        self._endInstantly = False
        self._cleanup_timer = None

        # final message
        if success:
            print(f"Félicitations! Vous avez réussi le mini-jeu: {self._name}")
        else:
            print(f"Vous avez échoué le mini-jeu: {self._name}. Essayez encore!")
        
        del self

    # -- Utilities / helpers --
    def getCenterXY(self):
        return (WIDTH/2, HEIGHT/2)  # Placeholder for center position

    #  mob methods
    def add_mob(self, mob):
        self._mobs.append(mob)

    def add_object(self, obj):
        self._objects.append(obj)

    #  Timer methods
    def update_timer(self):
        timer = self.getTimer()
        timeLimit = self.getTimeLimit()

        timer += self.gerRefreshRatePeriod()
        self._timer = timer
        if timer >= timeLimit:
            return True # time's up
        return False

    def reset_timer(self):
        self._timer = 0

    def getTimer(self):
        return self._timer

    def getTimeLimit(self):
        return self._time_limit

    # Loop methods
    def winCondition(self): # ⚠️ Definir dans le mini-jeu ⚠️
        return False

    def getRefreshRate(self):
        return MiniGame.refresh_rate

    def gerRefreshRatePeriod(self):
        return 1 / self.getRefreshRate()

    def loop(self):
        if self._endInstantly:
            return  # Exit if the game has been ended instantly

        self.checkControls() # keep original control checks for in-game controls
        if not self._hasStarted:
            return  # Do not proceed if the game hasn't started

        refreshDelay = self.gerRefreshRatePeriod()
        end = self.update_timer()

        if (end):
            win = self.winCondition()
            self.end(win)
            return  # End the loop

        for mob in self._mobs:
            mob.loop()
        # Store timer reference so we can cancel it later
        self._loop_timer = threading.Timer(refreshDelay, self.loop)
        self._loop_timer.start()
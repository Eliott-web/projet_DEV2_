from pynput import keyboard
from .controls_getter import ControlsGetter

class ControlTypeZqsd(ControlsGetter):
    pass


    def checkControls(self):
        if not hasattr(self, '_listener'):
            self._listener = keyboard.Listener(on_press=self.on_press)
            self._listener.start()

    def on_press(self, key):
        try:
            if key.char == 'q':      # gauche
                self.left_pressed()
            if key.char == 'd':      # droite
                self.right_pressed()
            if key.char == 's':      # bas
                self.down_pressed()
            if key.char == 'z':      # haut
                self.up_pressed()
        except AttributeError:
            # Ignore les touches spéciales (shift, ctrl, etc.)
            pass


    def left_pressed(self): # En gros les gars faut le définir dans le mini-jeu
        print("Left pressed!")

    def right_pressed(self):
        print("Right pressed!")

    def down_pressed(self):
        print("Down pressed!")

    def up_pressed(self):
        print("Up pressed!")
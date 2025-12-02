from pynput import keyboard
from .controls_getter import ControlsGetter

class ControlTypeSpace(ControlsGetter):
    pass


    def checkControls(self):
        if not hasattr(self, '_listener'):
            self._listener = keyboard.Listener(on_press=self.on_press)
            self._listener.start()

    def on_press(self, key):
        if key == keyboard.Key.space:
            self.space_pressed()

    def space_pressed(self): # En gros les gars faut le définir dans le mini-jeu
        print("Spacebar pressed!")
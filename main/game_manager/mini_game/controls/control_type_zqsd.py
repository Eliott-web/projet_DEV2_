from pynput import keyboard
from .controls_getter import ControlsGetter

class ControlTypeSpace(ControlsGetter):
    pass


    def checkControls(self):
        if not hasattr(self, '_listener'):
            self._listener = keyboard.Listener(on_press=self.on_press)
            self._listener.start()

    def on_press(self, key):
        if key == keyboard.Key.left:
            self.left_pressed()
        if key == keyboard.Key.right:
            self.right_pressed()
        if key == keyboard.Key.down:
            self.down_pressed()
        if key == keyboard.Key.up:
            self.up_pressed()

    def left_pressed(self): # En gros les gars faut le définir dans le mini-jeu
        print("Left pressed!")

    def right_pressed(self):
        print("Right pressed!")

    def down_pressed(self):
        print("Down pressed!")

    def up_pressed(self):
        print("Up pressed!")
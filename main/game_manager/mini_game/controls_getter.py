from pynput import keyboard

class ControlsGetter:
    pass


    def checkControls(self):
        if not hasattr(self, '_listener'):
            self._listener = keyboard.Listener(on_press=self.on_press)
            self._listener.start()

    def on_press(self, key):
        if key == keyboard.Key.space:
            self.space_pressed()

        elif key == keyboard.Key.left:
            self.left_pressed()

    def space_pressed(self):
        print("Spacebar pressed!")

    def left_pressed(self):
        print("Left arrow pressed!")
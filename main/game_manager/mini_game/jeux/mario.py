
from main.game_manager.mini_game.entities.mobs.koopa import Koopa
from main.game_manager.mini_game.entities.mobs.mario import Mario
from main.game_manager.mini_game.entities.objets.ground import Ground
from main.gui.widget.image import ImageWidget
from main.main import widget_manager
from ..controls.control_type_space import ControlTypeSpace
from ..mini_game import MiniGame
from ..entities.mobs.mob import Mob

class MiniGameMario(MiniGame, ControlTypeSpace):

    def __init__(self):
        super().__init__("Mario Jump", "Sautez au dessus des tortues!")
        
        self._jumps = 0
        self._mario = None
    
    def winCondition(self):
        return True

    def space_pressed(self):
        self._jumps += 1

    def start(self):
        print("Démarrage du mini-jeu Mario Jump!")
        self.ajouterObj()
        super().start()

    def ajouterObj(self):
        center = self.getCenterXY()
        self.build_background()

        koopa_y = center[1] + 200

        x_offset = 300
        koopa1 = Koopa((center[0] + x_offset, koopa_y))
        self.add_mob(koopa1)
        koopa2 = Koopa((center[0] - x_offset, koopa_y))
        self.add_mob(koopa2)
        koopa2.set_sens_inverse(True)
        koopa_size_y = koopa1.get_hitbox_size()[1]

        mario = Mario((center[0], koopa_y))
        self.add_mob(mario)
        self._mario = mario

        self.build_plat(koopa_y,koopa_size_y)
        
        
        print(f"Koopa created at: {center}")

    def build_background(self):
        center = self.getCenterXY()
        sky = ImageWidget("assets/background/mario_sky.png",center,(center[0]*2,center[1]*2),
                                      anchor="center",on_click=lambda w: None)
        self.add_object(sky)

        pipeM = 0.2
        pipeX = 963 * pipeM
        pipeY = 1037 * pipeM
        pipeSize = (pipeX,pipeY)
        pipePosition = (center[0], center[1] + 200)
        pipeOffset = 400
        pipe1 = ImageWidget("assets/background/pipe.png",(pipePosition[0] + pipeOffset, pipePosition[1]),pipeSize,
                                      anchor="center",on_click=lambda w: None)
        self.add_object(pipe1)
        pipe2 = ImageWidget("assets/background/pipe.png",(pipePosition[0] - pipeOffset, pipePosition[1]),pipeSize,
                                      anchor="center",on_click=lambda w: None)
        self.add_object(pipe2)

    def build_plat(self,koopa_y,koopa_size_y):
        center = self.getCenterXY()

        size = (center[0]*2, 700)
        platform_y = koopa_y + size[1] - (koopa_size_y * 2)
        platform_position = (center[0], platform_y)

        platform = Ground(platform_position, size)

        platform_sprite = ImageWidget("assets/background/mario_ground.png",platform_position,size=size,
                                      anchor="center",on_click=lambda w: None)
        platform.set_image(platform_sprite)

        self.add_object(platform)


    def getMario(self):
        return self._mario
    
    def loop(self): # boucle de jeu si vous en avez besoin de customiser
        mario = self.getMario()
        if mario.has_touched_koopa():
            self.endInstantly(False)
        #print(f"Jump! Total jumps: {self._jumps}") # truc custom

        super().loop()

    def space_pressed(self):
        mario = self.getMario()
        mario.jump()
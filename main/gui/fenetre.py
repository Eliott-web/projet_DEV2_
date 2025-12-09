import pygame
import sys

from main.main import widget_manager

# Remove these duplicate imports since they're already in the class definitions
# from main.gui.fenetre import WIDTH, add_image
# from main.gui.widget.image import ImageWidget
# from main.main import widget_manager
# from ..controls.control_type_space import ControlTypeSpace
# from ..mini_game import MiniGame
# from ..entities.mobs.mob import Mob

fps = 60
refreshDelay = 1 / fps

pygame.init()

# --- Configuration écran ---
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Fenêtre borderless")

def start():
    screen.fill((0,0,0))
    '''
    # Create and start the mini-game
    mini_game = MiniGameMario()
    mini_game.start()  # This will add the ImageWidget
    '''
    loop()  # Start the main loop

def loop():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        dt = clock.tick(fps) / 1000.0
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Handle space key for the mini-game
                    pass
            # Pass events to widgets
            widget_manager.handle_event(event)
        
        # Update widgets
        widget_manager.update_all(dt)
        
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Draw widgets
        widget_manager.draw_all(screen)
        
        pygame.display.flip()
        
        clock.tick(fps)
    
    # Clean shutdown
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start()
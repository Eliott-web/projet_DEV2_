import pygame
import sys

fps = 60
refreshDelay = 1 / fps

pygame.init()

# Get screen info BEFORE checking GUI mode
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Initialize screen as None initially
screen = None

def start():
    from main.main import isGuiMode

    global screen
    
    if isGuiMode():
        # Create window only if GUI mode is enabled
        screen = pygame.display.set_mode((WIDTH, HEIGHT), 0)
        pygame.display.set_caption("Fenêtre borderless")
        screen.fill((0,0,0))
        loop()  # Start the main loop with display
    else:
        # Run in headless/background mode
        print(f"Running in background mode. Screen resolution: {WIDTH}x{HEIGHT}")
        background_loop()

def background_loop():
    """Run the application without displaying a window"""
    clock = pygame.time.Clock()
    running = True
    
    while running:
        dt = clock.tick(fps) / 1000.0
        
        # Handle events (minimal event checking in background)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update widgets even without display
        from main.main import widget_manager
        widget_manager.update_all(dt)

        widget_manager.draw_all(screen)
        
        # No drawing needed in background mode
        
        # Optional: Reduce CPU usage when idle
        # if not widget_manager.has_active_widgets():
        #     pygame.time.wait(10)
    
    # Clean shutdown
    pygame.quit()
    sys.exit()

def loop():
    """Original main loop with display"""
    clock = pygame.time.Clock()
    running = True
    
    while running:
        from main.main import widget_manager
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
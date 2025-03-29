import pygame

class InputHandler:
    def __init__(self, game):
        self.game = game
    
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.game.state == "PLAYING":
                    if event.key == pygame.K_UP:
                        self.game.pacman.set_next_direction((0, -1))
                    elif event.key == pygame.K_RIGHT:
                        self.game.pacman.set_next_direction((1, 0))
                    elif event.key == pygame.K_DOWN:
                        self.game.pacman.set_next_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.game.pacman.set_next_direction((-1, 0))
                
                elif self.game.state in ["INTRO", "GAME_OVER"]:
                    # Start game on any key press
                    if event.key == pygame.K_RETURN:
                        self.game.start_game()
                
                # Global keys
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                elif event.key == pygame.K_p:
                    self.game.toggle_pause()
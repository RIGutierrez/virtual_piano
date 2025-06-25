import pygame
import piano_lists as pl
from pygame import mixer


class PianoApp:
    def __init__(self):
        pygame.init()
        pygame.mixer.set_num_channels(50)
        
        # Initialize fonts
        self.font = pygame.font.Font('assets/Terserah.ttf', 48)
        self.medium_font = pygame.font.Font('assets/Terserah.ttf', 28)
        self.small_font = pygame.font.Font('assets/Terserah.ttf', 16)
        self.real_small_font = pygame.font.Font('assets/Terserah.ttf', 10)
        
        # App settings
        self.fps = 60
        self.width = 52 * 35
        self.height = 400
        self.screen = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption('My Python Piano')
        
        self.running = True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self):
        pass  # Add update logic here in future
    
    def render(self):
        self.screen.fill('gray')
        # Add rendering logic here in future
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            clock.tick(self.fps)
        
        pygame.quit()


if __name__ == "__main__":
    app = PianoApp()
    app.run()
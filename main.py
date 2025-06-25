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
        
        # Piano state
        self.active_whites = []
        self.active_blacks = []
        self.white_keys = []
        self.black_keys = []

        # Piano notes and sounds
        self.left_hand = pl.left_hand
        self.right_hand = pl.right_hand
        self.piano_notes = pl.piano_notes
        self.white_notes = pl.white_notes
        self.black_notes = pl.black_notes
        self.black_labels = pl.black_labels
        
        # Load sounds
        self.white_sounds = self.load_sounds(self.white_notes)
        self.black_sounds = self.load_sounds(self.black_notes)
        
        self.running = True

    def load_sounds(self, notes):
        """Load sound files for the given notes"""
        sounds = []
        for note in notes:
            sounds.append(mixer.Sound(f'assets\\notes\\{note}.wav'))
        return sounds   

    def draw_piano(self):
        white_rects = []
        # Draw white keys
        for i in range(52):
            rect = pygame.draw.rect(self.screen, 'white', [i * 35, self.height - 300, 35, 300], 0, 2)
            white_rects.append(rect)
            pygame.draw.rect(self.screen, 'black', [i * 35, self.height - 300, 35, 300], 2, 2)
            key_label = self.small_font.render(pl.white_notes[i], True, 'black')
            self.screen.blit(key_label, (i * 35 + 3, self.height - 20))
        
        # Draw black keys
        skip_count = 0
        last_skip = 2
        skip_track = 2
        black_rects = []
        
        for i in range(36):
            rect = pygame.draw.rect(self.screen, 'black', 
                                  [23 + (i * 35) + (skip_count * 35), self.height - 300, 24, 200], 0, 2)
            
            # Highlight active black keys
            for q in range(len(self.active_blacks)):
                if self.active_blacks[q][0] == i:
                    if self.active_blacks[q][1] > 0:
                        pygame.draw.rect(self.screen, 'green', 
                                       [23 + (i * 35) + (skip_count * 35), self.height - 300, 24, 200], 2, 2)
                        self.active_blacks[q][1] -= 1

            key_label = self.real_small_font.render(pl.black_labels[i], True, 'white')
            self.screen.blit(key_label, (25 + (i * 35) + (skip_count * 35), self.height - 120))
            black_rects.append(rect)

            # Skip pattern for black keys
            skip_track += 1
            if last_skip == 2 and skip_track == 3:
                last_skip = 3
                skip_track = 0
                skip_count += 1
            elif last_skip == 3 and skip_track == 2:
                last_skip = 2
                skip_track = 0
                skip_count += 1

        # Highlight active white keys
        for i in range(len(self.active_whites)):
            if self.active_whites[i][1] > 0:
                j = self.active_whites[i][0]
                pygame.draw.rect(self.screen, 'green', [j * 35, self.height - 100, 35, 100], 2, 2)
                self.active_whites[i][1] -= 1

        return white_rects, black_rects
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_key_press(event.pos)
    def handle_key_press(self, pos):
        """Handle piano key press events"""
        black_key = False
        
        # Check black keys first
        for i in range(len(self.black_keys)):
            if self.black_keys[i].collidepoint(pos):
                self.black_sounds[i].play(0, 1000)
                black_key = True
                self.active_blacks.append([i, 30])
                break  # No need to check other keys if black key was pressed
        
        # Check white keys only if no black key was pressed
        if not black_key:
            for i in range(len(self.white_keys)):
                if self.white_keys[i].collidepoint(pos):
                    self.white_sounds[i].play(0, 1000)
                    self.active_whites.append([i, 30])
                    break
    
    def update(self):
        pass  # Add update logic here in future
    
    def render(self):
        self.screen.fill('gray')
        self.white_keys, self.black_keys = self.draw_piano()
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
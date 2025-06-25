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
        self.left_oct = 4
        self.right_oct = 5

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

        # Initialize keyboard mappings
        self.update_key_mappings()
        
        self.running = True

    def load_sounds(self, notes):
        """Load sound files for the given notes"""
        sounds = []
        for note in notes:
            sounds.append(mixer.Sound(f'assets\\notes\\{note}.wav'))
        return sounds 

    def update_key_mappings(self):
        """Update keyboard mappings when octaves change"""
        self.left_dict = {
            'Z': f'C{self.left_oct}', 'S': f'C#{self.left_oct}',
            'X': f'D{self.left_oct}', 'D': f'D#{self.left_oct}',
            'C': f'E{self.left_oct}', 'V': f'F{self.left_oct}',
            'G': f'F#{self.left_oct}', 'B': f'G{self.left_oct}',
            'H': f'G#{self.left_oct}', 'N': f'A{self.left_oct}',
            'J': f'A#{self.left_oct}', 'M': f'B{self.left_oct}'
        }
        
        self.right_dict = {
            'R': f'C{self.right_oct}', '5': f'C#{self.right_oct}',
            'T': f'D{self.right_oct}', '6': f'D#{self.right_oct}',
            'Y': f'E{self.right_oct}', 'U': f'F{self.right_oct}',
            '8': f'F#{self.right_oct}', 'I': f'G{self.right_oct}',
            '9': f'G#{self.right_oct}', 'O': f'A{self.right_oct}',
            '0': f'A#{self.right_oct}', 'P': f'B{self.right_oct}'
        }
    
    def draw_hands(self):
        """Draw the hand position indicators"""
        # Left hand
        pygame.draw.rect(self.screen, 'dark gray', [(self.left_oct * 245) - 175, self.height - 60, 245, 30], 0, 4)
        pygame.draw.rect(self.screen, 'black', [(self.left_oct * 245) - 175, self.height - 60, 245, 30], 4, 4)
        
        # Right hand
        pygame.draw.rect(self.screen, 'dark gray', [(self.right_oct * 245) - 175, self.height - 60, 245, 30], 0, 4)
        pygame.draw.rect(self.screen, 'black', [(self.right_oct * 245) - 175, self.height - 60, 245, 30], 4, 4)
        
        # Draw key labels for both hands
        self.draw_hand_labels(self.left_oct, self.left_hand)
        self.draw_hand_labels(self.right_oct, self.right_hand)

    def draw_hand_labels(self, octave, hand):
        """Draw the key labels for a hand"""
        base_x = (octave * 245) - 165
        y_pos = self.height - 55
        
        # White key labels
        labels = [
            (hand[0], -0), (hand[2], -35), (hand[4], -70), 
            (hand[5], -105), (hand[7], -140), (hand[9], -175), 
            (hand[11], -210)
        ]
        
        # Black key labels
        black_labels = [
            (hand[1], -17), (hand[3], -52), 
            (hand[6], -122), (hand[8], -157), (hand[10], -192)
        ]
        
        for label, offset in labels:
            text = self.small_font.render(label, True, 'white')
            self.screen.blit(text, (base_x - offset, y_pos))
            
        for label, offset in black_labels:
            text = self.small_font.render(label, True, 'black')
            self.screen.blit(text, (base_x - offset, y_pos))

    def draw_piano(self):
        white_rects = []
        # Draw white keys
        for i in range(52):
            rect = pygame.draw.rect(self.screen, 'white', [i * 35, self.height - 300, 35, 300], 0, 2)
            white_rects.append(rect)
            pygame.draw.rect(self.screen, 'black', [i * 35, self.height - 300, 35, 300], 2, 2)
            key_label = self.small_font.render(self.white_notes[i], True, 'black')
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

            key_label = self.real_small_font.render(self.black_labels[i], True, 'white')
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

        return white_rects, black_rects, self.active_whites, self.active_blacks
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

            if event.type == pygame.TEXTINPUT:
                self.handle_key_press(event.text.upper())

            if event.type == pygame.KEYDOWN:
                self.handle_octave_change(event.key)
    
    def handle_mouse_click(self, pos):
        """Handle piano key press events"""
        black_key = False
        
        # Check black keys first
        for i in range(len(self.black_keys)):
            if self.black_keys[i].collidepoint(pos):
                self.black_sounds[i].play(0, 1000)
                black_key = True
                self.active_blacks.append([i, 30])
                break  
        
        # Check white keys only if no black key was pressed
        if not black_key:
            for i in range(len(self.white_keys)):
                if self.white_keys[i].collidepoint(pos):
                    self.white_sounds[i].play(0, 1000)
                    self.active_whites.append([i, 30])
                    break
    
    def handle_key_press(self, key):
        """Handle piano key press via keyboard"""
        if key in self.left_dict:
            note = self.left_dict[key]
            self.play_note(note)
        elif key in self.right_dict:
            note = self.right_dict[key]
            self.play_note(note)

    def handle_octave_change(self, key):
        """Adjust octaves based on arrow key presses"""
        changed = False
        if key == pygame.K_RIGHT and self.right_oct < 8:
            self.right_oct += 1
            changed = True
        elif key == pygame.K_LEFT and self.right_oct > 0:
            self.right_oct -= 1
            changed = True
        elif key == pygame.K_UP and self.left_oct < 8:
            self.left_oct += 1
            changed = True
        elif key == pygame.K_DOWN and self.left_oct > 0:
            self.left_oct -= 1
            changed = True
            
        if changed:
            self.update_key_mappings()
    
    def play_note(self, note):
        """Play the corresponding note and highlight the key"""
        if note[1] == '#':  # Black key
            index = self.black_labels.index(note)
            self.black_sounds[index].play(0, 1000)
            self.active_blacks.append([index, 30])
        else:  # White key
            index = self.white_notes.index(note)
            self.white_sounds[index].play(0, 1000)
            self.active_whites.append([index, 30])
    
    def update(self):
        pass 
    
    def render(self):
        self.screen.fill('gray')
        self.white_keys, self.black_keys, self.active_whites, self.active_blacks = self.draw_piano()
        self.draw_hands()
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
import pygame
import random
import math
import sys

# --- Game Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60
# ... code...
WORLD_IMAGE = pygame.image.load("world.jpg")
WORLD_IMAGE = pygame.transform.scale(WORLD_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
# ... code...

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
LIGHT_GREY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
SKY_BLUE = (135, 206, 235)
OVERLAY_COLOR = (0, 0, 0)  # Changed overlay color to dark blue

# --- Initialize Pygame and Mixer ---
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Color Realm")
clock = pygame.time.Clock()

# --- Sound Effects ---
try:
    sound_correct = pygame.mixer.Sound('correct.wav')
    sound_incorrect = pygame.mixer.Sound('incorrect.wav')
    sound_complete = pygame.mixer.Sound('complete.wav')
except pygame.error:
    print("Sound files not found. The game will run without sound effects.")
    sound_correct = None
    sound_incorrect = None
    sound_complete = None

# --- Fonts ---
font_lg = pygame.font.Font(None, 74)
font_md = pygame.font.Font(None, 48)
font_sm = pygame.font.Font(None, 32)
font_xs = pygame.font.Font(None, 24)

def draw_text(surface, text, font, color, x, y):
    """Draws text on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    """Player character class."""
    def __init__(self):
        super().__init__()
        self.size = 30
        self.colors = [WHITE, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, CYAN]
        self.color_index = 0
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.colors[self.color_index])
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.5
        self.jump_power = -18
        self.is_jumping = False
        self.on_platform = False
        self.can_move_left = True
        self.can_move_right = True

    def update(self):
        """Updates player position and state."""
        self.speed_y += self.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Basic screen boundaries
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.is_jumping = False
            self.on_platform = False
            self.speed_y = 0

    def jump(self):
        """Makes the player jump."""
        if not self.is_jumping or self.on_platform:
            self.speed_y = self.jump_power
            self.is_jumping = True
            self.on_platform = False

    def set_on_platform(self):
        """Sets the player's state to be on a platform."""
        self.is_jumping = False
        self.on_platform = True
        self.speed_y = 0
    def move_left(self):
        """Moves the player left."""
        if self.can_move_left:
            self.speed_x = -5

    def move_right(self):
        """Moves the player right."""
        if self.can_move_right:
            self.speed_x = 5
    def stop_moving(self):
        """Stops the player's horizontal movement."""
        self.speed_x = 0

    def next_color(self):
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.image.fill(self.colors[self.color_index])

    def prev_color(self):
        self.color_index = (self.color_index - 1) % len(self.colors)
        self.image.fill(self.colors[self.color_index])

class Platform(pygame.sprite.Sprite):
    """Moving platform class."""
    def __init__(self, x, y, width, height, move_range, speed):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(LIGHT_GREY)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.move_range = move_range
        self.speed = speed
        self.direction = 1

    def update(self):
        """Updates platform position."""
        self.rect.x += self.speed * self.direction
        if self.rect.right > self.start_x + self.move_range or self.rect.left < self.start_x:
            self.direction *= -1

# --- Puzzle Classes ---
class ColorPuzzle:
    """Represents a color combination puzzle."""
    def __init__(self):
        self.target_color = self.get_random_color()
        self.is_solved = False

    def get_random_color(self):
        """Returns a random color from the predefined list."""
        colors = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, CYAN]
        return random.choice(colors)

    def check_solution(self, player_color):
        """Checks if the player's color matches the target color."""
        if player_color == self.target_color:
            self.is_solved = True
            if sound_correct:
                sound_correct.play()
            return True
        else:
            if sound_incorrect:
                sound_incorrect.play()
            return False


class TimePuzzle:
    """Represents a time-based moving platform puzzle."""
    def __init__(self):
        self.is_solved = False
        self.platforms = pygame.sprite.Group()
        self.create_platforms()
    
    def create_platforms(self):
        """Creates the moving platforms for the puzzle."""
        self.platforms.empty()
        num_platforms = 7  # More platforms for easier jumps
        platform_width = 140  # Wider platforms
        platform_height = 22
        vertical_gap = 80     # Smaller gap for easier jumps
        for i in range(num_platforms):
            platform_x = random.randint(60, SCREEN_WIDTH - platform_width - 60)
            platform_y = SCREEN_HEIGHT - 120 - (i * vertical_gap)
            move_range = random.randint(80, 200)  # Moderate movement
            speed = random.choice([1, 2])         # Slower speed for easier landing
            platform = Platform(platform_x, platform_y, platform_width, platform_height, move_range, speed)
            self.platforms.add(platform)
    def check_completion(self, player_y):
        """Checks if the player has reached the end of the puzzle."""
        if player_y < 100:  # Player reaches the top
            self.is_solved = True
            if sound_complete:
                sound_complete.play()
            return True
        return False

# --- Game States ---
def show_instructions():
    """Displays the instruction screen."""
    instructions = [
        "Welcome to the Color Realm!",
        "Your goal is to bring color back to the world.",
        "Solve two types of puzzles to clear the shadows.",
        "",
        "Color Puzzle: Match the target color with the player.",
        "Movement: Use Arrow Keys (Left/Right) to move.",
        "Jump: Use Space Bar to jump.",
        "Time Puzzle: Navigate moving platforms to the top.",
        "",
        "Press any key to begin..."
    ]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                running = False

        screen.fill(BLACK)  # Changed background to black for better contrast
        draw_text(screen, "Instructions", font_lg, YELLOW, SCREEN_WIDTH // 2, 50)  # Changed font color to yellow
        
        y_offset = 150
        for line in instructions:
            draw_text(screen, line, font_md, CYAN, SCREEN_WIDTH // 2, y_offset)  # Changed font color to cyan
            y_offset += 50

        pygame.display.flip()
        clock.tick(FPS)

def game_loop():
    """Main game loop."""
    show_instructions()

    # Create game objects
    player = Player()
    
    # Generate a set of unique puzzles
    puzzles = []
    num_puzzles = 5 # Total number of puzzles to clear the world
    for _ in range(num_puzzles):
        puzzle_type = random.choice(['color', 'time'])
        if puzzle_type == 'color':
            puzzles.append(ColorPuzzle())
        else:
            puzzles.append(TimePuzzle())

    current_puzzle_index = 0
    
    running = True
    while running:
        # --- Handle Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_a:
                    player.prev_color()
                if event.key == pygame.K_d:
                    player.next_color()
                # Add this to allow restarting after completion
                if event.key == pygame.K_r and current_puzzle_index >= len(puzzles):
                    return game_loop()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.speed_x < 0:
                    player.stop_moving()
                if event.key == pygame.K_RIGHT and player.speed_x > 0:
                    player.stop_moving()
    

        # --- Update Game State ---
        player.update()

        # Check if all puzzles are solved
        # ... code...
        # Check if all puzzles are solved
        # ... code...
        if current_puzzle_index >= len(puzzles):
            screen.blit(WORLD_IMAGE, (0, 0))
            draw_text(screen, "The World is Full of Natural Colors!", font_lg, YELLOW, SCREEN_WIDTH // 2, 100)
            draw_text(screen, "Press 'R' to Restart", font_md, CYAN, SCREEN_WIDTH // 2, 180)
            pygame.display.flip()
            clock.tick(FPS)
            continue
# ... code...


        # Get the current puzzle
        current_puzzle = puzzles[current_puzzle_index]

        # --- Drawing ---
        screen.fill(SKY_BLUE)

        # Draw current puzzle elements and apply puzzle logic
        if isinstance(current_puzzle, ColorPuzzle):
            # Draw color combination puzzle elements
            pygame.draw.circle(screen, current_puzzle.target_color, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100), 50)
            draw_text(screen, "Target Color", font_sm, YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 170)
            draw_text(screen, "Match the player color with this!", font_sm, CYAN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

            # Puzzle solving logic: check if player color matches target color
            if player.image.get_at((0, 0))[:3] == current_puzzle.target_color and not current_puzzle.is_solved:
                current_puzzle.is_solved = True
                if sound_correct:
                    sound_correct.play()
                current_puzzle_index += 1
                player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        
        elif isinstance(current_puzzle, TimePuzzle):
            current_puzzle.platforms.update()
            
            # Check for player collision with platforms
            player.on_platform = False
            player.can_move_left = True
            player.can_move_right = True
            
            for platform in current_puzzle.platforms:
                if pygame.sprite.collide_rect(player, platform):
                   if player.speed_y >= 0 and player.rect.bottom - platform.rect.top < 25 and player.rect.top < platform.rect.top:
                        player.rect.bottom = platform.rect.top
                        player.set_on_platform()
                        player.rect.x += platform.speed * platform.direction
            
            # Check for puzzle completion
            if current_puzzle.check_completion(player.rect.y):
                current_puzzle_index += 1
                player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
            
            current_puzzle.platforms.draw(screen)

        # Draw player
        screen.blit(player.image, player.rect)
        
        # --- Draw the gray overlay to show progression ---
        grey_alpha = max(0, 120 - (100 // num_puzzles) * current_puzzle_index)  # More transparent
        if grey_alpha > 0:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((*OVERLAY_COLOR, grey_alpha))
            screen.blit(overlay, (0, 0))


        # Update display and tick clock
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
# ...existing code...
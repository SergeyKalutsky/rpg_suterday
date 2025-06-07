import pygame

# Initialize Pygame
pygame.init()
pygame.font.init()  # Initialize font module

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Starter")


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = (255, 0, 0)  # Red color

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Button(GameObject):
    def __init__(self, x, y, width, height, path):
        super().__init__(x, y, width, height, path)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    

class Hero(GameObject):
    def __init__(self, x, y, width, height, path):
        super().__init__(x, y, width, height, path)
        self.health = 100
        self.score = 0
        self.standing_images = []
        self.moving_left_images = []
        self.moving_right_images = []
        self.attack_images = []
        for i in range(1, 11):
            img = pygame.image.load(f"images/warrior/{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (width, height))
            self.standing_images.append(img)
        for i in range(11, 18):
            img = pygame.image.load(f"images/warrior/{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (width, height))
            self.moving_right_images.append(img)
        for i in range(11, 18):
            img = pygame.image.load(f"images/warrior/{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (width, height))
            self.moving_left_images.append(pygame.transform.flip(img, True, False))
        for i in range(41, 48):
            img = pygame.image.load(f"images/warrior/{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (width, height))
            self.attack_images.append(img)
        self.state = "standing"  # Initial state of the hero
        self.current_image_index = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if self.state == "standing":
            self.current_image_index = (self.current_image_index + 1) % len(self.standing_images)
            self.image = self.standing_images[self.current_image_index]
        elif self.state == "moving_left":
            self.current_image_index = (self.current_image_index + 1) % len(self.moving_left_images)
            self.image = self.moving_left_images[self.current_image_index]
        elif self.state == "moving_right":
            self.current_image_index = (self.current_image_index + 1) % len(self.moving_right_images)
            self.image = self.moving_right_images[self.current_image_index]
        elif self.state == "attacking":
            self.current_image_index = (self.current_image_index + 1) % len(self.attack_images)
            self.image = self.attack_images[self.current_image_index]
            if self.current_image_index == 0:
                self.state = "standing"    

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 5
            self.state = "moving_left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 5
            self.state = "moving_right"
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= 5
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += 5
        else:
            self.state = "standing"
    
    def attack(self):
        self.state = "attacking"
        self.current_image_index = 0

        


class Monster(GameObject):
    def __init__(self, x, y, width, height, path):
        super().__init__(x, y, width, height, path)
        self.health = 50
        self.animation_images = []
        
        # Load monster animation images (1-8)
        for i in range(1, 9):
            img = pygame.image.load(f"images/moster/{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (width, height))
            self.animation_images.append(img)
        
        self.current_image_index = 0
        self.animation_speed = 0.2  # Controls how fast the animation plays
        self.animation_counter = 0

    def update(self):
        # Update animation
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.current_image_index = (self.current_image_index + 1) % len(self.animation_images)
            self.image = self.animation_images[self.current_image_index]
            self.animation_counter = 0


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game states
MENU_STATE = "menu"
GAME_STATE = "game"
SETTINGS_STATE = "settings"

# Game loop
running = True
clock = pygame.time.Clock()
current_state = MENU_STATE

bg = GameObject(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, "images/bg.png")
start_btn = Button(100, 100, 200, 50, "images/game_btn.png")
exit_btn = Button(100, 200, 200, 50, "images/exit_btn.png")
settings_btn = Button(100, 300, 200, 50, "images/settings_btn.png")
hero = Hero(300, 400, 100, 100, "images/warrior/1.png")
monster = Monster(500, 200, 80, 80, "images/moster/1.png")

def handle_menu_events(event):
    global current_state, running
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if start_btn.is_clicked(mouse_pos):
            current_state = GAME_STATE
        elif exit_btn.is_clicked(mouse_pos):
            running = False
        elif settings_btn.is_clicked(mouse_pos):
            current_state = SETTINGS_STATE

def handle_game_events(event):
    global current_state
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            current_state = MENU_STATE

def handle_settings_events(event):
    global current_state
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            current_state = MENU_STATE

def draw_menu():
    bg.draw(screen)
    start_btn.draw(screen)
    exit_btn.draw(screen)
    settings_btn.draw(screen)

def draw_game():
    bg.draw(screen)
    hero.update()
    hero.draw(screen)
    monster.update()
    monster.draw(screen)

def draw_settings():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render("Settings - Press ESC to return", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(text, text_rect)

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hero.attack()
                
        if event.type == pygame.QUIT:
            running = False
        
        if current_state == MENU_STATE:
            handle_menu_events(event)
        elif current_state == GAME_STATE:
            handle_game_events(event)
        elif current_state == SETTINGS_STATE:
            handle_settings_events(event)
        

    # Draw based on current state
    if current_state == MENU_STATE:
        draw_menu()
    elif current_state == GAME_STATE:
        draw_game()
    elif current_state == SETTINGS_STATE:
        draw_settings()

    pygame.display.flip() 
    pygame.display.update()  # Update the display
    clock.tick(20)

# Quit Pygame
pygame.quit()
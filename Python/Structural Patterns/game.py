import pygame
import sys
import random
from abc import ABC, abstractmethod
from enum import Enum

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Design Patterns Game")
clock = pygame.time.Clock()

###############################################
# ADAPTER PATTERN IMPLEMENTATION
###############################################
# Abstract Input Handler (Target)
class InputHandler(ABC):
    @abstractmethod
    def get_movement(self) -> tuple:
        """Return movement vector (dx, dy)"""
        pass

# Concrete WASD Input Handler
class WASDInputHandler(InputHandler):
    def get_movement(self) -> tuple:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_d]:
            dx = 1
        return (dx, dy)

# Concrete Arrow Keys Input Handler
class ArrowKeysInputHandler(InputHandler):
    def get_movement(self) -> tuple:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        return (dx, dy)

# Concrete NumPad Input Handler
class NumPadInputHandler(InputHandler):
    def get_movement(self) -> tuple:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_KP8]:
            dy = -1
        if keys[pygame.K_KP2]:
            dy = 1
        if keys[pygame.K_KP4]:
            dx = -1
        if keys[pygame.K_KP6]:
            dx = 1
        return (dx, dy)

# Input Controller that uses the adapter pattern to handle different input types
class InputController:
    def __init__(self):
        # Default to WASD
        self.current_handler = WASDInputHandler()
        self.handlers = {
            "wasd": WASDInputHandler(),
            "arrows": ArrowKeysInputHandler(),
            "numpad": NumPadInputHandler()
        }
    
    def set_input_handler(self, handler_name):
        if handler_name in self.handlers:
            self.current_handler = self.handlers[handler_name]
    
    def get_movement(self):
        return self.current_handler.get_movement()

###############################################
# DECORATOR PATTERN IMPLEMENTATION
###############################################
# Abstract Player (Component)
class Player(ABC):
    @abstractmethod
    def update(self, movement):
        pass
    
    @abstractmethod
    def draw(self, surface):
        pass
    
    @abstractmethod
    def get_speed(self):
        pass
    
    @abstractmethod
    def get_health(self):
        pass
    
    @abstractmethod
    def get_rect(self):
        pass
    
    @abstractmethod
    def get_money(self):
        pass
    
    @abstractmethod
    def add_money(self, amount):
        pass

# Concrete Player (ConcreteComponent)
class BasicPlayer(Player):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 5
        self.health = 100
        self.money = 0
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self, movement):
        dx, dy = movement
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Keep player on screen
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))
        
        # Update rect
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)
    
    def get_speed(self):
        return self.speed
    
    def get_health(self):
        return self.health
    
    def get_rect(self):
        return self.rect
    
    def get_money(self):
        return self.money
    
    def add_money(self, amount):
        self.money += amount

# Abstract Player Decorator (Decorator)
class PlayerDecorator(Player):
    def __init__(self, player):
        self.player = player
    
    def update(self, movement):
        self.player.update(movement)
    
    def draw(self, surface):
        self.player.draw(surface)
    
    def get_speed(self):
        return self.player.get_speed()
    
    def get_health(self):
        return self.player.get_health()
    
    def get_rect(self):
        return self.player.get_rect()
    
    def get_money(self):
        return self.player.get_money()
    
    def add_money(self, amount):
        self.player.add_money(amount)

# Concrete Decorators
class SpeedBoostDecorator(PlayerDecorator):
    def __init__(self, player, boost_amount=1):
        super().__init__(player)
        self.boost_amount = boost_amount
    
    def get_speed(self):
        return self.player.get_speed() + self.boost_amount
    
    def draw(self, surface):
        # Call the parent draw method
        self.player.draw(surface)
        # Add a green outline to show speed boost
        pygame.draw.rect(surface, GREEN, self.get_rect(), 2)

class HealthBoostDecorator(PlayerDecorator):
    def __init__(self, player, boost_amount=20):
        super().__init__(player)
        self.boost_amount = boost_amount
    
    def get_health(self):
        return self.player.get_health() + self.boost_amount
    
    def draw(self, surface):
        # Call the parent draw method
        self.player.draw(surface)
        # Add a red outline to show health boost
        pygame.draw.rect(surface, RED, self.get_rect(), 2)

###############################################
# GAME OBJECTS
###############################################
class Coin:
    def __init__(self):
        self.radius = 15
        self.reset_position()
    
    def reset_position(self):
        self.x = random.randint(self.radius, SCREEN_WIDTH - self.radius)
        self.y = random.randint(self.radius, SCREEN_HEIGHT - self.radius)
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                               self.radius * 2, self.radius * 2)
    
    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.radius)

class Enemy:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.reset_position()
    
    def reset_position(self):
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(0, SCREEN_HEIGHT - self.height)
        self.dx = random.choice([-2, -1, 1, 2])
        self.dy = random.choice([-2, -1, 1, 2])
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
        # Bounce off walls
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.dx *= -1
        if self.y <= 0 or self.y >= SCREEN_HEIGHT - self.height:
            self.dy *= -1
            
        # Update rect
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, surface):
        # Draw a red triangle
        p1 = (self.x, self.y + self.height)
        p2 = (self.x + self.width, self.y + self.height)
        p3 = (self.x + self.width // 2, self.y)
        pygame.draw.polygon(surface, RED, [p1, p2, p3])

###############################################
# FACADE PATTERN IMPLEMENTATION
###############################################
class GameState(Enum):
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    UPGRADE_MENU = 3
    GAME_OVER = 4

class GameFacade:
    def __init__(self):
        # Initialize game objects
        self.player = BasicPlayer(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.input_controller = InputController()
        self.coins = [Coin() for _ in range(5)]
        self.enemies = [Enemy() for _ in range(3)]
        self.game_state = GameState.MENU
        self.font = pygame.font.SysFont(None, 36)
        
        # Track upgrade costs
        self.speed_upgrade_cost = 10
        self.health_upgrade_cost = 15
    
    def start_game(self):
        """Start a new game"""
        self.game_state = GameState.PLAYING
        self.player = BasicPlayer(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.coins = [Coin() for _ in range(5)]
        self.enemies = [Enemy() for _ in range(3)]
    
    def pause_game(self):
        """Pause the current game"""
        if self.game_state == GameState.PLAYING:
            self.game_state = GameState.PAUSED
        elif self.game_state == GameState.PAUSED:
            self.game_state = GameState.PLAYING
    
    def show_upgrade_menu(self):
        """Show the upgrade menu"""
        if self.game_state in [GameState.PLAYING, GameState.PAUSED]:
            self.game_state = GameState.UPGRADE_MENU
    
    def return_to_game(self):
        """Return to the game from any menu"""
        if self.game_state in [GameState.MENU, GameState.UPGRADE_MENU, GameState.PAUSED]:
            self.game_state = GameState.PLAYING
    
    def apply_speed_upgrade(self):
        """Apply speed upgrade to player"""
        if self.player.get_money() >= self.speed_upgrade_cost:
            self.player.add_money(-self.speed_upgrade_cost)
            self.player = SpeedBoostDecorator(self.player)
            self.speed_upgrade_cost += 5  # Increase cost for next upgrade
    
    def apply_health_upgrade(self):
        """Apply health upgrade to player"""
        if self.player.get_money() >= self.health_upgrade_cost:
            self.player.add_money(-self.health_upgrade_cost)
            self.player = HealthBoostDecorator(self.player)
            self.health_upgrade_cost += 5  # Increase cost for next upgrade
    
    def change_input_method(self, method):
        """Change the input method"""
        self.input_controller.set_input_handler(method)
    
    def update(self):
        """Update game state"""
        if self.game_state == GameState.PLAYING:
            # Get movement from current input handler (Adapter Pattern)
            movement = self.input_controller.get_movement()
            
            # Update player (potentially decorated with upgrades)
            self.player.update(movement)
            
            # Update enemies
            for enemy in self.enemies:
                enemy.update()
                
                # Check for collision with player
                if enemy.rect.colliderect(self.player.get_rect()):
                    # Decrease player health
                    self.player.health -= 10

                    # Game over if health is depleted
                    if self.player.get_health() < 10:
                        self.game_state = GameState.GAME_OVER
                    # Otherwise just restart the enemy
                    else:
                        enemy.reset_position()
            
            # Check for coin collection
            for coin in self.coins:
                if coin.rect.colliderect(self.player.get_rect()):
                    self.player.add_money(5)  # Add 5 coins
                    coin.reset_position()
    
    def draw(self, surface):
        """Draw the current game state"""
        surface.fill(BLACK)
        
        if self.game_state == GameState.MENU:
            # Draw menu
            title = self.font.render("Design Patterns Game", True, WHITE)
            start_text = self.font.render("Press ENTER to start", True, WHITE)
            
            surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
            surface.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))
            
        elif self.game_state == GameState.PLAYING or self.game_state == GameState.PAUSED:
            # Draw game objects
            for coin in self.coins:
                coin.draw(surface)
                
            for enemy in self.enemies:
                enemy.draw(surface)
                
            self.player.draw(surface)
            
            # Draw HUD
            money_text = self.font.render(f"Money: {self.player.get_money()}", True, WHITE)
            health_text = self.font.render(f"Health: {self.player.get_health()}", True, WHITE)
            speed_text = self.font.render(f"Speed: {self.player.get_speed()}", True, WHITE)
            
            surface.blit(money_text, (10, 10))
            surface.blit(health_text, (10, 50))
            surface.blit(speed_text, (10, 90))
            
            # Draw controls info
            controls_text = self.font.render("U: Upgrade Menu | P: Pause | 1-3: Change Controls", True, WHITE)
            surface.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, 10))
            
            if self.game_state == GameState.PAUSED:
                # Draw pause overlay
                pause_text = self.font.render("PAUSED", True, WHITE)
                surface.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 
                                         SCREEN_HEIGHT // 2 - pause_text.get_height() // 2))
                
        elif self.game_state == GameState.UPGRADE_MENU:
            # Draw upgrade menu
            title = self.font.render("Upgrade Menu", True, WHITE)
            speed_text = self.font.render(f"1: Speed Boost (Cost: {self.speed_upgrade_cost})", True, WHITE)
            health_text = self.font.render(f"2: Health Boost (Cost: {self.health_upgrade_cost})", True, WHITE)
            back_text = self.font.render("ESC: Back to Game", True, WHITE)
            money_text = self.font.render(f"Your Money: {self.player.get_money()}", True, YELLOW)
            
            surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            surface.blit(speed_text, (SCREEN_WIDTH // 2 - speed_text.get_width() // 2, 200))
            surface.blit(health_text, (SCREEN_WIDTH // 2 - health_text.get_width() // 2, 250))
            surface.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 350))
            surface.blit(money_text, (SCREEN_WIDTH // 2 - money_text.get_width() // 2, 150))
            
        elif self.game_state == GameState.GAME_OVER:
            # Draw game over screen
            game_over_text = self.font.render("GAME OVER", True, RED)
            restart_text = self.font.render("Press ENTER to play again", True, WHITE)
            
            surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
            surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 300))

###############################################
# MAIN GAME LOOP
###############################################
def main():
    # Create game facade
    game = GameFacade()
    
    # Main game loop
    running = True
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                # Handle key presses based on game state
                if game.game_state == GameState.MENU:
                    if event.key == pygame.K_RETURN:
                        game.start_game()
                        
                elif game.game_state == GameState.PLAYING:
                    if event.key == pygame.K_p:
                        game.pause_game()
                    elif event.key == pygame.K_u:
                        game.show_upgrade_menu()
                    elif event.key == pygame.K_1:
                        game.change_input_method("wasd")
                    elif event.key == pygame.K_2:
                        game.change_input_method("arrows")
                    elif event.key == pygame.K_3:
                        game.change_input_method("numpad")
                        
                elif game.game_state == GameState.PAUSED:
                    if event.key == pygame.K_p:
                        game.pause_game()
                    elif event.key == pygame.K_u:
                        game.show_upgrade_menu()
                        
                elif game.game_state == GameState.UPGRADE_MENU:
                    if event.key == pygame.K_ESCAPE:
                        game.return_to_game()
                    elif event.key == pygame.K_1:
                        game.apply_speed_upgrade()
                    elif event.key == pygame.K_2:
                        game.apply_health_upgrade()
                        
                elif game.game_state == GameState.GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        game.start_game()
        
        # Update and render the game
        game.update()
        game.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
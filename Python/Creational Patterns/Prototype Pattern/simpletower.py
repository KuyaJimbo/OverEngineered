import pygame
import sys
import random
import copy
from abc import ABC, abstractmethod

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
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Prototype interface (abstract class)
class TowerPrototype(ABC):
    @abstractmethod
    def clone(self):
        pass
    
    @abstractmethod
    def draw(self, screen):
        pass
    
    @abstractmethod
    def update(self, enemies):
        pass
    
    def is_clicked(self, mouse_x, mouse_y):
        """Check if tower is clicked"""
        distance = ((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2) ** 0.5
        return distance <= self.radius

# Concrete Prototype 1: Laser Tower
class LaserTower(TowerPrototype):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.radius = 20
        self.attack_radius = 150
        self.damage = 2
        self.attack_cooldown = 30
        self.current_cooldown = 0
        self.color = RED
        self.target = None
        self.attack_line = None
        self.name = "Laser Tower"

    def clone(self):
        return copy.deepcopy(self)
    
    def draw(self, screen):
        # Draw tower
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Draw attack radius (when selected)
        if game_state.selected_tower == self or game_state.tower_to_place and isinstance(game_state.tower_to_place, LaserTower):
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.attack_radius, 1)
        # Draw attack line
        if self.attack_line:
            pygame.draw.line(screen, YELLOW, (self.x, self.y), self.attack_line, 2)
        
        # Draw name below tower
        font = pygame.font.SysFont(None, 24)
        name_text = font.render(self.name, True, BLACK)
        screen.blit(name_text, (self.x - 50, self.y + 30))
    
    def update(self, enemies):
        # Reset attack line
        self.attack_line = None
        
        # Reduce cooldown
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
            return
        
        # Find closest enemy in range
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance <= self.attack_radius and distance < min_distance:
                closest_enemy = enemy
                min_distance = distance
        
        # Attack if enemy found
        if closest_enemy:
            closest_enemy.health -= self.damage
            self.current_cooldown = self.attack_cooldown
            self.attack_line = (closest_enemy.x, closest_enemy.y)

# Concrete Prototype 2: Cannon Tower
class CannonTower(TowerPrototype):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.radius = 25
        self.attack_radius = 200
        self.damage = 5
        self.attack_cooldown = 60
        self.current_cooldown = 0
        self.color = BLUE
        self.explosion_radius = 50
        self.explosion = None
        self.explosion_duration = 5
        self.current_explosion = 0
        self.name = "Cannon Tower"

    def clone(self):
        return copy.deepcopy(self)
    
    def draw(self, screen):
        # Draw tower
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Draw attack radius (when selected)
        if game_state.selected_tower == self or game_state.tower_to_place and isinstance(game_state.tower_to_place, CannonTower):
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.attack_radius, 1)
        # Draw explosion
        if self.explosion and self.current_explosion > 0:
            pygame.draw.circle(screen, YELLOW, self.explosion, self.explosion_radius, 1)
            
        # Draw name below tower
        font = pygame.font.SysFont(None, 24)
        name_text = font.render(self.name, True, BLACK)
        screen.blit(name_text, (self.x - 50, self.y + 30))
    
    def update(self, enemies):
        # Handle explosion animation
        if self.current_explosion > 0:
            self.current_explosion -= 1
            if self.current_explosion == 0:
                self.explosion = None
        
        # Reduce cooldown
        if self.current_cooldown > 0:
            self.current_cooldown -= 1
            return
        
        # Find closest enemy in range
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance <= self.attack_radius and distance < min_distance:
                closest_enemy = enemy
                min_distance = distance
        
        # Attack if enemy found
        if closest_enemy:
            # Area damage
            self.explosion = (closest_enemy.x, closest_enemy.y)
            self.current_explosion = self.explosion_duration
            
            # Apply damage to all enemies in explosion radius
            for enemy in enemies:
                dx = enemy.x - closest_enemy.x
                dy = enemy.y - closest_enemy.y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                
                if distance <= self.explosion_radius:
                    enemy.health -= self.damage
            
            self.current_cooldown = self.attack_cooldown

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(1.0, 3.0)
        self.health = 10
        self.radius = 15
        self.color = PURPLE
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Health bar
        health_bar_length = 30
        health_ratio = self.health / 10
        health_bar = health_ratio * health_bar_length
        
        pygame.draw.rect(screen, RED, (self.x - health_bar_length//2, self.y - 20, health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (self.x - health_bar_length//2, self.y - 20, health_bar, 5))
    
    def update(self):
        self.y += self.speed

# Client: Game State Manager (Manages prototypes and game state)
class GameState:
    def __init__(self):
        # Initialize prototype towers on the field
        self.towers = [
            LaserTower(100, 500),
            CannonTower(200, 500)
        ]
        
        self.enemies = []
        self.spawn_cooldown = 60
        self.current_spawn = 0
        self.score = 0
        self.lives = 10
        
        # Tower placement
        self.selected_tower = None
        self.tower_to_place = None
        
        # Game message
        self.message = "Click on a tower to clone it"
        self.message_timer = 180  # 3 seconds at 60 FPS
    
    def clone_tower(self, tower):
        """Clone a tower to create a new instance"""
        self.tower_to_place = tower.clone()
        self.message = "Click on the field to place the cloned tower"
        self.message_timer = 180
    
    def place_tower(self, x, y):
        """Place the cloned tower on the field"""
        if self.tower_to_place:
            self.tower_to_place.x = x
            self.tower_to_place.y = y
            self.towers.append(self.tower_to_place)
            self.tower_to_place = None
            self.selected_tower = None
            self.message = "Tower placed! Click on a tower to clone it"
            self.message_timer = 180
    
    def update(self):
        """Update game state"""
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
        
        # Spawn enemies
        if self.current_spawn <= 0:
            x = random.randint(50, SCREEN_WIDTH - 50)
            self.enemies.append(Enemy(x, 0))
            self.current_spawn = self.spawn_cooldown
        else:
            self.current_spawn -= 1
        
        # Update towers
        for tower in self.towers:
            tower.update(self.enemies)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Enemy reached bottom
            if enemy.y > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.lives -= 1
            
            # Enemy died
            elif enemy.health <= 0:
                self.enemies.remove(enemy)
                self.score += 10
    
    def draw(self, screen):
        """Draw game elements"""
        # Draw game area
        screen.fill(GRAY)
        
        # Draw towers
        for tower in self.towers:
            tower.draw(screen)
            
            # Highlight selected tower
            if tower == self.selected_tower:
                pygame.draw.circle(screen, GREEN, (tower.x, tower.y), tower.radius + 5, 2)
        
        # Draw temporary tower when placing
        if self.tower_to_place:
            self.tower_to_place.draw(screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # Draw UI text
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        lives_text = font.render(f"Lives: {self.lives}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        
        # Draw instruction message
        if self.message_timer > 0:
            message_text = font.render(self.message, True, BLACK)
            message_bg = pygame.Surface((message_text.get_width() + 20, message_text.get_height() + 10))
            message_bg.fill(WHITE)
            message_bg.set_alpha(200)
            screen.blit(message_bg, (SCREEN_WIDTH//2 - message_bg.get_width()//2, 50))
            screen.blit(message_text, (SCREEN_WIDTH//2 - message_text.get_width()//2, 55))

# Initialize game state
game_state = GameState()

def main():
    # Initialize screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense - Prototype Pattern")
    clock = pygame.time.Clock()
    
    # Game loop
    while True:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # If we're placing a tower
                if game_state.tower_to_place:
                    game_state.place_tower(mouse_x, mouse_y)
                
                # Otherwise, check if we clicked on a tower to clone it
                else:
                    for tower in game_state.towers:
                        if tower.is_clicked(mouse_x, mouse_y):
                            game_state.selected_tower = tower
                            game_state.clone_tower(tower)
                            break
            
            elif event.type == pygame.MOUSEMOTION and game_state.tower_to_place:
                # Update temp tower position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                game_state.tower_to_place.x = mouse_x
                game_state.tower_to_place.y = mouse_y
        
        # Update game state
        game_state.update()
        
        # Check game over
        if game_state.lives <= 0:
            font = pygame.font.SysFont(None, 60)
            game_over_text = font.render("GAME OVER", True, RED)
            screen.fill(BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()
        
        # Draw
        screen.fill(BLACK)
        game_state.draw(screen)
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()
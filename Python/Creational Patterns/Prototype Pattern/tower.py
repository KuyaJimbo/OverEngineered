import pygame
import sys
import math
import copy
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 40
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
DARK_GREEN = (0, 100, 0)

# Game States
GAME_STATE_PLAYING = 0
GAME_STATE_GAME_OVER = 1
GAME_STATE_VICTORY = 2

# Prototype Pattern Interface
class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass

# Tower base class implementing Prototype
class Tower(Prototype):
    def __init__(self, x: int, y: int, radius: int, damage: int, cooldown: int, 
                 cost: int, color: Tuple[int, int, int], name: str):
        self.x = x
        self.y = y
        self.radius = radius  # Attack radius
        self.damage = damage
        self.cooldown = cooldown  # Attack cooldown in frames
        self.cooldown_counter = 0
        self.cost = cost
        self.color = color
        self.name = name
        self.level = 1
        self.target = None
        
    def clone(self):
        """Implementation of the Prototype pattern clone method"""
        return copy.deepcopy(self)
    
    def upgrade(self):
        """Upgrade the tower"""
        self.level += 1
        self.damage = int(self.damage * 1.5)
        self.radius += 20
        self.cooldown = max(10, int(self.cooldown * 0.8))
        return self.cost // 2  # Upgrade cost is half of the original
    
    def can_attack(self):
        """Check if the tower can attack"""
        if self.cooldown_counter <= 0:
            return True
        return False
    
    def find_target(self, enemies: List["Enemy"]) -> Optional["Enemy"]:
        """Find the closest enemy in range"""
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
            if distance <= self.radius and distance < min_distance:
                closest_enemy = enemy
                min_distance = distance
                
        return closest_enemy
    
    def attack(self, enemies: List["Enemy"]) -> int:
        """Attack enemies in range"""
        if not self.can_attack():
            self.cooldown_counter -= 1
            return 0
        
        self.target = self.find_target(enemies)
        if self.target:
            self.target.health -= self.damage
            self.cooldown_counter = self.cooldown
            return self.damage
        
        return 0
    
    def draw(self, screen: pygame.Surface):
        """Draw the tower"""
        # Draw attack radius (partially transparent)
        radius_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(radius_surface, (*self.color, 50), (self.radius, self.radius), self.radius)
        screen.blit(radius_surface, (self.x - self.radius, self.y - self.radius))
        
        # Draw the tower
        pygame.draw.circle(screen, self.color, (self.x, self.y), 15)
        
        # Draw tower level
        font = pygame.font.SysFont(None, 20)
        level_text = font.render(str(self.level), True, BLACK)
        screen.blit(level_text, (self.x - 5, self.y - 7))
        
        # Draw attack line if targeting an enemy
        if self.target and self.target.is_alive():
            pygame.draw.line(screen, RED, (self.x, self.y), (self.target.x, self.target.y), 2)

# Concrete Tower Types
class BasicTower(Tower):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x=x, y=y, radius=100, damage=10, cooldown=30, 
                         cost=50, color=BLUE, name="Basic Tower")

class SniperTower(Tower):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x=x, y=y, radius=200, damage=30, cooldown=60, 
                         cost=100, color=RED, name="Sniper Tower")

class BomberTower(Tower):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x=x, y=y, radius=80, damage=15, cooldown=45, 
                         cost=75, color=YELLOW, name="Bomber Tower")
        
    def attack(self, enemies: List["Enemy"]) -> int:
        """Bomber attacks all enemies in radius"""
        if not self.can_attack():
            self.cooldown_counter -= 1
            return 0
        
        enemies_in_range = []
        for enemy in enemies:
            distance = math.sqrt((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2)
            if distance <= self.radius:
                enemies_in_range.append(enemy)
                
        if enemies_in_range:
            total_damage = 0
            for enemy in enemies_in_range:
                enemy.health -= self.damage
                total_damage += self.damage
            self.cooldown_counter = self.cooldown
            return total_damage
        
        return 0

# Enemy class
class Enemy:
    def __init__(self, path: List[Tuple[int, int]], speed: float, health: int, value: int, color: Tuple[int, int, int]):
        self.path = path
        self.path_index = 0
        self.x, self.y = path[0]
        self.speed = speed
        self.max_health = health
        self.health = health
        self.value = value  # Money gained when killed
        self.color = color
        
    def update(self) -> bool:
        """Update enemy position. Returns True if reached the end."""
        if self.path_index >= len(self.path) - 1:
            return True
        
        target_x, target_y = self.path[self.path_index + 1]
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        if distance < self.speed:
            self.x, self.y = target_x, target_y
            self.path_index += 1
        else:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
        return False
    
    def is_alive(self) -> bool:
        """Check if the enemy is still alive."""
        return self.health > 0
    
    def draw(self, screen: pygame.Surface):
        """Draw the enemy."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)
        
        # Health bar
        health_ratio = max(0, self.health / self.max_health)
        width = 20
        height = 5
        pygame.draw.rect(screen, RED, (int(self.x) - width // 2, int(self.y) - 20, width, height))
        pygame.draw.rect(screen, GREEN, (int(self.x) - width // 2, int(self.y) - 20, int(width * health_ratio), height))

# Enemy Factory 
class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type: str, path: List[Tuple[int, int]]) -> Enemy:
        if enemy_type == "basic":
            return Enemy(path, 2.0, 50, 10, GREEN)
        elif enemy_type == "fast":
            return Enemy(path, 3.5, 30, 15, YELLOW)
        elif enemy_type == "tank":
            return Enemy(path, 1.0, 150, 25, RED)
        else:
            raise ValueError(f"Unknown enemy type: {enemy_type}")

# Wave Manager to control enemy spawning
class WaveManager:
    def __init__(self):
        self.current_wave = 0
        self.waves = []
        self.spawn_timer = 0
        self.enemy_index = 0
        self.active = False
        self.spawn_delay = 60  # Frames between enemy spawns
        
    def add_wave(self, enemies: List[str]):
        """Add a wave of enemies."""
        self.waves.append(enemies)
    
    def start_wave(self):
        """Start the next wave."""
        if self.current_wave < len(self.waves):
            self.active = True
            self.enemy_index = 0
            self.spawn_timer = 0
            return True
        return False
    
    def update(self, path: List[Tuple[int, int]]) -> Optional[Enemy]:
        """Update wave manager, returns a new enemy if it's time to spawn one."""
        if not self.active:
            return None
        
        self.spawn_timer += 1
        
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            
            if self.enemy_index < len(self.waves[self.current_wave]):
                enemy_type = self.waves[self.current_wave][self.enemy_index]
                self.enemy_index += 1
                return EnemyFactory.create_enemy(enemy_type, path)
            elif self.enemy_index >= len(self.waves[self.current_wave]):
                self.active = False
                self.current_wave += 1
                
        return None
    
    def is_finished(self) -> bool:
        """Check if all waves are completed."""
        return self.current_wave >= len(self.waves) and not self.active

# Tower Defense Game Class
class TowerDefenseGame:
    def __init__(self):
        # Initialize screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense - Prototype Pattern")
        self.clock = pygame.time.Clock()
        
        # Game variables
        self.money = 200
        self.lives = 20
        self.score = 0
        self.game_state = GAME_STATE_PLAYING
        
        # Create path
        self.path = [
            (0, 300), (200, 300), (200, 150), (400, 150), 
            (400, 450), (600, 450), (600, 300), (800, 300)
        ]
        
        # Initialize wave manager and create waves
        self.wave_manager = WaveManager()
        self.setup_waves()
        
        # Game objects
        self.towers: List[Tower] = []
        self.enemies: List[Enemy] = []
        self.tower_prototypes: Dict[str, Tower] = {
            "basic": BasicTower(),
            "sniper": SniperTower(),
            "bomber": BomberTower()
        }
        
        # UI variables
        self.selected_tower_type = None
        self.dragging_tower = None
        self.selected_tower = None
        self.grid_visible = True
        
    def setup_waves(self):
        """Setup the enemy waves."""
        # Wave 1: 10 basic enemies
        self.wave_manager.add_wave(["basic"] * 10)
        
        # Wave 2: 15 enemies, mix of basic and fast
        wave2 = ["basic"] * 8 + ["fast"] * 7
        self.wave_manager.add_wave(wave2)
        
        # Wave 3: 20 enemies, including tanks
        wave3 = ["basic"] * 10 + ["fast"] * 7 + ["tank"] * 3
        self.wave_manager.add_wave(wave3)
        
        # Wave 4: 25 enemies with more tanks
        wave4 = ["basic"] * 10 + ["fast"] * 10 + ["tank"] * 5
        self.wave_manager.add_wave(wave4)
        
        # Wave 5: 30 enemies, difficult mix
        wave5 = ["basic"] * 10 + ["fast"] * 12 + ["tank"] * 8
        self.wave_manager.add_wave(wave5)
        
    def start_wave(self):
        """Start the next wave."""
        if not self.wave_manager.active:
            return self.wave_manager.start_wave()
        return False
    
    def get_grid_position(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Convert screen position to grid position."""
        x, y = pos
        grid_x = (x // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
        grid_y = (y // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
        return grid_x, grid_y
    
    def is_position_valid(self, pos: Tuple[int, int]) -> bool:
        """Check if tower can be placed at position."""
        x, y = pos
        
        # Check if position is on screen
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT:
            return False
        
        # Check if position is too close to path
        for path_x, path_y in self.path:
            distance = math.sqrt((x - path_x) ** 2 + (y - path_y) ** 2)
            if distance < 30:  # Buffer distance from path
                return False
        
        # Check if position overlaps with another tower
        for tower in self.towers:
            distance = math.sqrt((x - tower.x) ** 2 + (y - tower.y) ** 2)
            if distance < 40:  # Buffer distance between towers
                return False
                
        return True
    
    def select_tower_type(self, tower_type: str):
        """Select tower type to place."""
        if tower_type in self.tower_prototypes:
            self.selected_tower_type = tower_type
            self.selected_tower = None
            
            # Create a copy of the prototype for dragging
            prototype = self.tower_prototypes[tower_type]
            self.dragging_tower = prototype.clone()
        else:
            self.selected_tower_type = None
            self.dragging_tower = None
    
    def place_tower(self, pos: Tuple[int, int]) -> bool:
        """Place tower at position using the Prototype pattern."""
        if not self.selected_tower_type or not self.dragging_tower:
            return False
        
        grid_pos = self.get_grid_position(pos)
        
        if not self.is_position_valid(grid_pos):
            return False
        
        # Check if can afford the tower
        prototype = self.tower_prototypes[self.selected_tower_type]
        if self.money < prototype.cost:
            return False
        
        # Create new tower by cloning the prototype (Prototype Pattern)
        new_tower = prototype.clone()
        new_tower.x, new_tower.y = grid_pos
        
        self.towers.append(new_tower)
        self.money -= new_tower.cost
        
        return True
    
    def select_tower(self, pos: Tuple[int, int]) -> bool:
        """Select tower at position."""
        for tower in self.towers:
            distance = math.sqrt((pos[0] - tower.x) ** 2 + (pos[1] - tower.y) ** 2)
            if distance < 20:
                self.selected_tower = tower
                self.selected_tower_type = None
                self.dragging_tower = None
                return True
                
        self.selected_tower = None
        return False
    
    def upgrade_selected_tower(self) -> bool:
        """Upgrade the selected tower."""
        if not self.selected_tower:
            return False
        
        upgrade_cost = self.selected_tower.cost // 2
        
        if self.money >= upgrade_cost:
            self.money -= upgrade_cost
            self.selected_tower.upgrade()
            return True
            
        return False
    
    def sell_selected_tower(self) -> bool:
        """Sell the selected tower."""
        if not self.selected_tower:
            return False
        
        sell_value = int(self.selected_tower.cost * 0.7)  # 70% of the original cost
        self.money += sell_value
        self.towers.remove(self.selected_tower)
        self.selected_tower = None
        return True
    
    def process_events(self) -> bool:
        """Process input events. Return False to quit the game."""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Deselect tower or tower type
                    self.selected_tower_type = None
                    self.selected_tower = None
                    self.dragging_tower = None
                elif event.key == pygame.K_g:
                    # Toggle grid visibility
                    self.grid_visible = not self.grid_visible
                elif event.key == pygame.K_n:
                    # Start next wave
                    self.start_wave()
                elif event.key == pygame.K_u:
                    # Upgrade selected tower
                    self.upgrade_selected_tower()
                elif event.key == pygame.K_s:
                    # Sell selected tower
                    self.sell_selected_tower()
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    # Select tower type with number keys
                    tower_types = list(self.tower_prototypes.keys())
                    index = event.key - pygame.K_1
                    if 0 <= index < len(tower_types):
                        self.select_tower_type(tower_types[index])
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.selected_tower_type:
                        # Try to place tower
                        self.place_tower(mouse_pos)
                    else:
                        # Try to select tower
                        self.select_tower(mouse_pos)
                        
        # Update dragging tower position
        if self.dragging_tower:
            grid_pos = self.get_grid_position(mouse_pos)
            self.dragging_tower.x, self.dragging_tower.y = grid_pos
            
        return True
    
    def update(self):
        """Update game logic."""
        # Spawn new enemies
        new_enemy = self.wave_manager.update(self.path)
        if new_enemy:
            self.enemies.append(new_enemy)
        
        # Update enemies
        enemies_to_remove = []
        for enemy in self.enemies:
            reached_end = enemy.update()
            
            if reached_end:
                # Enemy reached the end of the path
                self.lives -= 1
                enemies_to_remove.append(enemy)
            elif not enemy.is_alive():
                # Enemy was killed
                self.money += enemy.value
                self.score += enemy.value
                enemies_to_remove.append(enemy)
                
        # Remove dead or finished enemies
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)
        
        # Update towers
        for tower in self.towers:
            tower.attack(self.enemies)
            
        # Check game over conditions
        if self.lives <= 0:
            self.game_state = GAME_STATE_GAME_OVER
            
        # Check victory condition
        if self.wave_manager.is_finished() and not self.enemies:
            self.game_state = GAME_STATE_VICTORY
    
    def draw_grid(self):
        """Draw the grid on the screen."""
        if not self.grid_visible:
            return
            
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, LIGHT_GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, LIGHT_GRAY, (0, y), (SCREEN_WIDTH, y))
    
    def draw_path(self):
        """Draw the enemy path."""
        if len(self.path) < 2:
            return
            
        # Draw path background
        for i in range(len(self.path) - 1):
            start_x, start_y = self.path[i]
            end_x, end_y = self.path[i + 1]
            
            # Calculate rectangle for this path segment
            if start_x == end_x:  # Vertical segment
                rect_x = start_x - 15
                rect_y = min(start_y, end_y)
                rect_width = 30
                rect_height = abs(end_y - start_y)
            else:  # Horizontal segment
                rect_x = min(start_x, end_x)
                rect_y = start_y - 15
                rect_width = abs(end_x - start_x)
                rect_height = 30
                
            pygame.draw.rect(self.screen, LIGHT_GRAY, (rect_x, rect_y, rect_width, rect_height))
            
        # Draw path borders
        for i in range(len(self.path) - 1):
            start = self.path[i]
            end = self.path[i + 1]
            
            # Draw the path edges
            pygame.draw.line(self.screen, DARK_GREEN, 
                            (start[0] - 15 if start[0] == end[0] else start[0], 
                             start[1] - 15 if start[1] == end[1] else start[1]),
                            (end[0] - 15 if start[0] == end[0] else end[0], 
                             end[1] - 15 if start[1] == end[1] else end[1]), 2)
            pygame.draw.line(self.screen, DARK_GREEN, 
                            (start[0] + 15 if start[0] == end[0] else start[0], 
                             start[1] + 15 if start[1] == end[1] else start[1]),
                            (end[0] + 15 if start[0] == end[0] else end[0], 
                             end[1] + 15 if start[1] == end[1] else end[1]), 2)
    
    def draw_ui(self):
        """Draw UI elements."""
        # Draw HUD
        font = pygame.font.SysFont(None, 30)
        money_text = font.render(f"Money: ${self.money}", True, GREEN)
        lives_text = font.render(f"Lives: {self.lives}", True, RED)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        wave_text = font.render(f"Wave: {self.wave_manager.current_wave + 1}/{len(self.wave_manager.waves)}", True, YELLOW)
        
        self.screen.blit(money_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
        self.screen.blit(score_text, (10, 70))
        self.screen.blit(wave_text, (10, 100))
        
        # Draw tower selection UI
        x_offset = 200
        for i, (tower_type, prototype) in enumerate(self.tower_prototypes.items()):
            # Draw tower icon
            icon_x = x_offset + i * 100
            icon_y = 20
            pygame.draw.circle(self.screen, prototype.color, (icon_x, icon_y), 15)
            
            # Draw tower cost
            cost_text = font.render(f"${prototype.cost}", True, WHITE)
            self.screen.blit(cost_text, (icon_x - 15, icon_y + 20))
            
            # Draw key hint
            key_text = font.render(f"{i+1}", True, YELLOW)
            self.screen.blit(key_text, (icon_x - 5, icon_y - 25))
            
            # Highlight selected tower type
            if self.selected_tower_type == tower_type:
                pygame.draw.circle(self.screen, WHITE, (icon_x, icon_y), 20, 2)
        
        # Draw help text
        help_font = pygame.font.SysFont(None, 20)
        help_texts = [
            "N: Next Wave",
            "G: Toggle Grid",
            "ESC: Cancel",
            "U: Upgrade Tower",
            "S: Sell Tower"
        ]
        
        for i, text in enumerate(help_texts):
            help_surface = help_font.render(text, True, WHITE)
            self.screen.blit(help_surface, (SCREEN_WIDTH - 150, 10 + i * 20))
        
        # Draw selected tower info
        if self.selected_tower:
            tower = self.selected_tower
            info_x = SCREEN_WIDTH - 150
            info_y = 150
            
            # Create info panel
            pygame.draw.rect(self.screen, GRAY, (info_x - 10, info_y - 10, 150, 160))
            
            info_font = pygame.font.SysFont(None, 22)
            info_texts = [
                f"Type: {tower.name}",
                f"Level: {tower.level}",
                f"Damage: {tower.damage}",
                f"Range: {tower.radius}",
                f"Cooldown: {tower.cooldown//10}s",
                f"Upgrade: ${tower.cost//2}",
                f"Sell: ${int(tower.cost * 0.7)}"
            ]
            
            for i, text in enumerate(info_texts):
                info_surface = info_font.render(text, True, WHITE)
                self.screen.blit(info_surface, (info_x, info_y + i * 20))
        
        # Draw next wave button
        if not self.wave_manager.active:
            pygame.draw.rect(self.screen, GREEN, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, 130, 30))
            next_wave_text = font.render("Next Wave (N)", True, BLACK)
            self.screen.blit(next_wave_text, (SCREEN_WIDTH - 145, SCREEN_HEIGHT - 45))
        else:
            # Draw wave progress
            wave_size = len(self.wave_manager.waves[self.wave_manager.current_wave])
            progress = self.wave_manager.enemy_index / wave_size
            pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, 130, 30))
            pygame.draw.rect(self.screen, GREEN, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, int(130 * progress), 30))
            progress_text = font.render(f"{self.wave_manager.enemy_index}/{wave_size}", True, BLACK)
            self.screen.blit(progress_text, (SCREEN_WIDTH - 145, SCREEN_HEIGHT - 45))
        
        # Draw dragging tower (preview)
        if self.dragging_tower:
            tower = self.dragging_tower
            # Draw semi-transparent radius circle
            radius_surface = pygame.Surface((tower.radius * 2, tower.radius * 2), pygame.SRCALPHA)
            valid_position = self.is_position_valid((tower.x, tower.y))
            color = (*tower.color, 100) if valid_position else (255, 0, 0, 100)
            pygame.draw.circle(radius_surface, color, (tower.radius, tower.radius), tower.radius)
            self.screen.blit(radius_surface, (tower.x - tower.radius, tower.y - tower.radius))
            
            # Draw the tower preview
            pygame.draw.circle(self.screen, tower.color if valid_position else RED, (tower.x, tower.y), 15)
    
    def draw_game_over(self):
        """Draw game over screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont(None, 72)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)
        
        restart_text = font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(restart_text, restart_rect)

    def draw_victory(self):
        """Draw victory screen."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont(None, 72)
        text = font.render("VICTORY!", True, GREEN)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)
        
        # Draw final score
        final_score_text = font.render(f"Final Score: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(final_score_text, final_score_rect)

        # Draw final money
        final_money_text = font.render(f"Final Money: ${self.money}", True, WHITE)
        final_money_rect = final_money_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(final_money_text, final_money_rect)

        # Draw final lives
        final_lives_text = font.render(f"Final Lives: {self.lives}", True, WHITE)
        final_lives_rect = final_lives_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(final_lives_text, final_lives_rect)

    
    def draw(self):
        """Draw game elements to the screen."""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw grid
        self.draw_grid()
        
        # Draw path
        self.draw_path()
        
        # Draw towers
        for tower in self.towers:
            tower.draw(self.screen)
            
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        # Draw UI
        self.draw_ui()
        
        # Draw game over or victory screen if needed
        if self.game_state == GAME_STATE_GAME_OVER:
            self.draw_game_over()
        elif self.game_state == GAME_STATE_VICTORY:
            self.draw_victory()
            
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        running = True
        while running:
            # Process events
            running = self.process_events()
            
            # Update game logic
            if self.game_state == GAME_STATE_PLAYING:
                self.update()
                
            # Draw everything
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(FPS)

# Main function
def main():
    game = TowerDefenseGame()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

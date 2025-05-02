import pygame
import random
import sys
from abc import ABC, abstractmethod
from enum import Enum

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Factory Pattern - Space Shooter")
clock = pygame.time.Clock()

# --- ENUM for Enemy ColorInfo ---
class ColorInfo(Enum):
    RED = ((255, 0, 0), 3, 1)      # High health, slow
    GREEN = ((0, 255, 0), 2, 2)    # Medium
    BLUE = ((0, 0, 255), 1, 3)     # Low health, fast

# --- Abstract Product ---
class Spawnable(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def get_rect(self):
        pass

# --- Concrete Products ---
class Enemy(Spawnable):
    def __init__(self, x, y, color_info):
        self.color, self.health, self.speed = color_info
        self.rect = pygame.Rect(x, y, 40, 40)

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def get_rect(self):
        return self.rect

class Asteroid(Spawnable):
    def __init__(self, x, y, speed):
        self.color = (128, 128, 128)
        self.speed = speed
        self.radius = 20
        self.x = x
        self.y = y

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

class Bullet(Spawnable):
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 20)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 100, 255), self.rect)
    
    def get_rect(self):
        return self.rect

# --- Abstract Factory ---
class Spawner(ABC):
    @abstractmethod
    def spawn(self) -> Spawnable:
        pass

# --- Concrete Factories ---
class EnemySpawner(Spawner):
    def spawn(self) -> Spawnable:
        x = random.randint(0, SCREEN_WIDTH - 40)
        color_info = random.choice(list(ColorInfo)).value
        return Enemy(x, 0, color_info)

class AsteroidSpawner(Spawner):
    def spawn(self) -> Spawnable:
        x = random.randint(20, SCREEN_WIDTH - 20)
        speed = random.randint(2, 5)
        return Asteroid(x, 0, speed)



class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50
        self.speed = 5
        self.width = 40
        self.height = 40
        self.bullets = []

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))

    def shoot(self):
        bullet = Bullet(self.x + self.width // 2 - 2, self.y)
        self.bullets.append(bullet)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if b.rect.y > -20]

    def draw(self, surface):
        # Draw triangle for the player
        pygame.draw.polygon(surface, (100, 200, 255), [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ])
        for bullet in self.bullets:
            bullet.draw(surface)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# --- Game Loop ---
def main():
    player = Player()
    spawnables = []

    enemy_spawner = EnemySpawner()
    asteroid_spawner = AsteroidSpawner()

    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, 500) # Every second call the spawn event

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SPAWN_EVENT:
                # FACTORY PATTERN USAGE HERE
                if random.random() < 0.6:
                    spawnables.append(enemy_spawner.spawn())
                else:
                    spawnables.append(asteroid_spawner.spawn())
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot()

        player.move(keys)
        player.update_bullets()

        # Update and draw spawnables
        for obj in spawnables:
            obj.update()
            obj.draw(screen)

        # Remove off-screen spawnables
        spawnables = [s for s in spawnables if s.get_rect().top <= SCREEN_HEIGHT]

        # Collision detection
        for obj in spawnables:
            if player.get_rect().colliderect(obj.get_rect()):
                print("Game Over!")
                running = False

        # Bullet collisions
        for bullet in player.bullets:
            for obj in spawnables:
                if bullet.rect.colliderect(obj.get_rect()):
                    # decrement the health of the enemy and remove the bullet
                    if isinstance(obj, Enemy):
                        obj.health -= 1
                        if obj.health <= 0:
                            spawnables.remove(obj)
                            # Optionally, you can add a score increment here
                    elif isinstance(obj, Asteroid):
                        spawnables.remove(obj)
                        # Optionally, you can add a score increment here
                    else:
                        # Handle other spawnable types if needed
                        pass
                    # Remove the bullet after collision
                    player.bullets.remove(bullet)

        player.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

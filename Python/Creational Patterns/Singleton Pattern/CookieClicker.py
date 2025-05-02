import pygame
import sys

# Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
LIGHT_GRAY = (200, 200, 200)

# GameManager Singleton Class
class GameManager:
    _instance = None
    
    # this method is called when the class is instantiated
    # this is different from __init__ which is called when the instance is created
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
            # Initialize the singleton instance
            cls._instance.total_cookies = 0
            cls._instance.cookies_per_second = 0
            cls._instance.cookies_per_click = 1
            cls._instance.upgrades = []
        return cls._instance
    
    # @classmethod ensures that this method can be called on the class itself, not just on instances of the class
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            return cls()
        return cls._instance
    
    def add_cookies(self, amount):
        self.total_cookies += amount
    
    def can_afford(self, price):
        return self.total_cookies >= price
    
    def spend_cookies(self, amount):
        self.total_cookies -= amount
    
    def add_cookies_per_second(self, amount):
        self.cookies_per_second += amount
    
    def update_cookies_per_second(self):
        """Recalculate cookies per second based on all upgrades"""
        self.cookies_per_second = 0
        for upgrade in self.upgrades:
            self.cookies_per_second += upgrade.value * upgrade.quantity
    
    def register_upgrade(self, upgrade):
        """Register an upgrade with the game manager"""
        self.upgrades.append(upgrade)
    
    def tick(self):
        """Process one game tick"""
        self.total_cookies += self.cookies_per_second / 60


# Cookie Class
class Cookie:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.game_manager = GameManager.get_instance()
    
    def draw(self):
        pygame.draw.circle(screen, BROWN, (self.x, self.y), self.radius)
    
    def clicked(self, pos):
        if ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5 <= self.radius:
            self.game_manager.add_cookies(self.game_manager.cookies_per_click)
            return True
        return False


# Upgrade Class
class Upgrade:
    def __init__(self, x, y, width, height, name, price, value):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.price = price
        self.value = value
        self.quantity = 0
        self.game_manager = GameManager.get_instance()
        self.game_manager.register_upgrade(self)

    def draw(self):
        pygame.draw.rect(screen, LIGHT_GRAY, (self.x, self.y, self.width, self.height))
        screen.blit(font.render(f"{self.name}: {self.quantity}", True, BLACK), (self.x + 10, self.y + 10))
        screen.blit(font.render(f"Price: {self.price}", True, BLACK), (self.x + 10, self.y + 40))
        screen.blit(font.render(f"Value: {self.value}/s", True, BLACK), (self.x + 10, self.y + 70))

    def clicked(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height
    
    def purchase(self):
        print(f"Attempting to purchase {self.name}")
        if self.game_manager.can_afford(self.price):
            self.game_manager.spend_cookies(self.price)
            self.quantity += 1
            self.price = int(self.price * 1.15)
            self.game_manager.update_cookies_per_second()
            print(f"Purchased {self.name}")
            return True
        else:
            print("Not enough cookies")
            return False


# Initialize the game manager singleton
game_manager = GameManager.get_instance()

# Create game objects
cookie = Cookie(WIDTH // 2, HEIGHT // 2, 50)
factory = Upgrade(WIDTH - 220, 220, 200, 100, "Factory", 50, 5)
grandma = Upgrade(WIDTH - 220, 100, 200, 100, "Grandma", 10, 1)

# Clock for framerate control
clock = pygame.time.Clock()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("Mouse Clicked")
            # Check if the cookie was clicked
            cookie.clicked(event.pos)
            
            # Check if upgrades were clicked
            if factory.clicked(event.pos):
                factory.purchase()
                
            if grandma.clicked(event.pos):
                grandma.purchase()

    # Update game state
    game_manager.tick()

    # Draw the game
    screen.fill(WHITE)
    cookie.draw()
    factory.draw()
    grandma.draw()

    # Display game stats
    screen.blit(font.render(f"Cookies: {int(game_manager.total_cookies)}", True, BLACK), (10, 10))
    screen.blit(font.render(f"Per second: {game_manager.cookies_per_second}", True, BLACK), (10, 50))
    screen.blit(font.render(f"Per click: {game_manager.cookies_per_click}", True, BLACK), (10, 90))

    pygame.display.flip()
    clock.tick(60)  # 60 FPS
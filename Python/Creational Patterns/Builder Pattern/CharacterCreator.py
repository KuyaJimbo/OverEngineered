import pygame
import sys
from abc import ABC, abstractmethod

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Character Creator - Builder Pattern")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)

# Font
font = pygame.font.SysFont(None, 28)
title_font = pygame.font.SysFont(None, 36)

# Product class
class Character:
    def __init__(self):
        self.character_class = None
        self.weapon = None
        self.armor = None
        self.skills = []
        self.color = None
        
    def display(self, screen, position):
        # Display character class and base shape
        if self.character_class:
            # Draw character body
            pygame.draw.rect(screen, self.color or BLACK, 
                            (position[0] - 25, position[1] - 25, 50, 80))
            
            # Draw character head
            pygame.draw.circle(screen, self.color or BLACK, 
                              (position[0], position[1] - 40), 20)
            
            # Draw class name
            text = font.render(self.character_class, True, WHITE)
            screen.blit(text, (position[0] - text.get_width() // 2, position[1] + 70))
        
        # Display weapon
        if self.weapon:
            weapon_text = font.render(f"Weapon: {self.weapon}", True, BLACK)
            screen.blit(weapon_text, (position[0] - 100, position[1] - 80))
            
            # Visual representation of weapon
            if "Staff" in self.weapon:
                pygame.draw.line(screen, BROWN, (position[0] + 30, position[1] - 30), 
                                (position[0] + 30, position[1] + 40), 5)
                pygame.draw.circle(screen, BLUE, (position[0] + 30, position[1] - 30), 8)
            elif "Sword" in self.weapon:
                pygame.draw.line(screen, GOLD, (position[0] + 30, position[1]), 
                                (position[0] + 60, position[1] - 20), 4)
                pygame.draw.line(screen, BLACK, (position[0] + 36, position[1] - 3), 
                                (position[0] + 40, position[1] - 3), 6)
            elif "Bow" in self.weapon:
                pygame.draw.arc(screen, BROWN, (position[0] + 25, position[1] - 20, 20, 50), 
                               1.5, 4.7, 3)
                pygame.draw.line(screen, BLACK, (position[0] + 35, position[1] - 15), 
                                (position[0] + 35, position[1] + 25), 1)
        
        # Display armor
        if self.armor:
            armor_text = font.render(f"Armor: {self.armor}", True, BLACK)
            screen.blit(armor_text, (position[0] - 100, position[1] - 50))
            
            # Visual cue for armor type
            if "Plate" in self.armor:
                pygame.draw.rect(screen, GOLD, (position[0] - 15, position[1] - 10, 30, 50), 2)
            elif "Robe" in self.armor:
                pygame.draw.rect(screen, PURPLE, (position[0] - 20, position[1] - 15, 40, 60), 1)
            elif "Leather" in self.armor:
                pygame.draw.rect(screen, BROWN, (position[0] - 18, position[1] - 12, 36, 55), 1)
        
        # Display skills
        if self.skills:
            for i, skill in enumerate(self.skills):
                skill_text = font.render(f"Skill: {skill}", True, BLACK)
                screen.blit(skill_text, (position[0] - 100, position[1] - 20 + i * 30))

# Builder Interface
class CharacterBuilder(ABC):
    @abstractmethod
    def set_class(self) -> None:
        pass
    
    @abstractmethod
    def set_weapon(self) -> None:
        pass
    
    @abstractmethod
    def set_armor(self) -> None:
        pass
    
    @abstractmethod
    def set_skills(self) -> None:
        pass
    
    @abstractmethod
    def get_result(self) -> Character:
        pass

# Concrete Builders
class WarriorBuilder(CharacterBuilder):
    def __init__(self):
        self.character = Character()
        self.character.color = RED
    
    def set_class(self) -> None:
        self.character.character_class = "Warrior"
    
    def set_weapon(self) -> None:
        self.character.weapon = "Great Sword"
    
    def set_armor(self) -> None:
        self.character.armor = "Plate Mail"
    
    def set_skills(self) -> None:
        self.character.skills = ["Charge", "Battle Cry"]
    
    def get_result(self) -> Character:
        return self.character

class MageBuilder(CharacterBuilder):
    def __init__(self):
        self.character = Character()
        self.character.color = BLUE
    
    def set_class(self) -> None:
        self.character.character_class = "Mage"
    
    def set_weapon(self) -> None:
        self.character.weapon = "Arcane Staff"
    
    def set_armor(self) -> None:
        self.character.armor = "Enchanted Robe"
    
    def set_skills(self) -> None:
        self.character.skills = ["Fireball", "Teleport"]
    
    def get_result(self) -> Character:
        return self.character

class ArcherBuilder(CharacterBuilder):
    def __init__(self):
        self.character = Character()
        self.character.color = GREEN
    
    def set_class(self) -> None:
        self.character.character_class = "Archer"
    
    def set_weapon(self) -> None:
        self.character.weapon = "Longbow"
    
    def set_armor(self) -> None:
        self.character.armor = "Leather Armor"
    
    def set_skills(self) -> None:
        self.character.skills = ["Quick Shot", "Eagle Eye"]
    
    def get_result(self) -> Character:
        return self.character

# Director
class CharacterDirector:
    def __init__(self, builder: CharacterBuilder):
        self.builder = builder
    
    def construct(self) -> None:
        self.builder.set_class()
        self.builder.set_weapon()
        self.builder.set_armor()
        self.builder.set_skills()
    
    def change_builder(self, builder: CharacterBuilder) -> None:
        self.builder = builder

# Button class for UI
class Button:
    def __init__(self, x, y, width, height, color, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.callback = callback
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()
            return True
        return False

# Client
class Game:
    def __init__(self):
        self.characters = []
        self.builders = {
            "warrior": WarriorBuilder(),
            "mage": MageBuilder(),
            "archer": ArcherBuilder()
        }
        self.director = CharacterDirector(self.builders["warrior"])

    def create_character(self, character_class: str) -> None:
        if character_class in self.builders:
            self.director.change_builder(self.builders[character_class])
            self.director.construct()
            character = self.director.builder.get_result()
            self.characters.append(character)
    
    def display_characters(self, screen):
        for i, character in enumerate(self.characters):
            position = (200 + i * 200, 300)
            character.display(screen, position)

# Main game function
def main():
    game = Game()
    
    # Create buttons
    buttons = [
        Button(100, 50, 150, 50, RED, "Create Warrior", lambda: game.create_character("warrior")),
        Button(300, 50, 150, 50, BLUE, "Create Mage", lambda: game.create_character("mage")),
        Button(500, 50, 150, 50, GREEN, "Create Archer", lambda: game.create_character("archer")),
        Button(300, 500, 150, 50, WHITE, "Reset", lambda: game.characters.clear())
    ]
    
    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.check_click(event.pos)
        
        # Clear the screen
        screen.fill((240, 240, 240))
        
        # Draw title
        title = title_font.render("Character Creator - Builder Pattern Demo", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 10))
        
        # Draw buttons
        for button in buttons:
            button.draw(screen)
        
        # Display characters
        game.display_characters(screen)
        
        # Draw instructions
        instructions = font.render("Click a button to create a character", True, BLACK)
        screen.blit(instructions, (SCREEN_WIDTH//2 - instructions.get_width()//2, 120))
        
        # Update the display
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
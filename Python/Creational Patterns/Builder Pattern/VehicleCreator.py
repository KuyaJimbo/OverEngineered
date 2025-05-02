import pygame
import sys
from abc import ABC, abstractmethod
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Vehicle Builder Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Font
font = pygame.font.SysFont(None, 36)

# Product class
class Vehicle:
    def __init__(self):
        self.engine = None
        self.chassis = None
        self.wheels = None
        self.color = None
        self.vehicle_type = None
        
    def display(self, screen, position):
        # Display engine
        if self.engine:
            pygame.draw.rect(screen, BLACK, (position[0], position[1], 80, 40))
            text = font.render(self.engine, True, WHITE)
            screen.blit(text, (position[0] + 10, position[1] + 10))
        
        # Display chassis
        if self.chassis:
            pygame.draw.rect(screen, self.color or BLACK, 
                             (position[0] - 40, position[1] + 50, 160, 60))
            text = font.render(self.chassis, True, WHITE)
            screen.blit(text, (position[0], position[1] + 60))
        
        # Display wheels
        if self.wheels:
            wheel_count = int(self.wheels.split()[0])
            for i in range(wheel_count):
                offset = 30 * i
                pygame.draw.circle(screen, BLACK, 
                                  (position[0] - 20 + offset, position[1] + 130), 15)

        # Display vehicle type
        if self.vehicle_type:
            text = font.render(f"Type: {self.vehicle_type}", True, BLACK)
            screen.blit(text, (position[0] - 40, position[1] - 40))

# Builder Interface
class VehicleBuilder(ABC):
    @abstractmethod
    def build_engine(self) -> None:
        pass
    
    @abstractmethod
    def build_chassis(self) -> None:
        pass
    
    @abstractmethod
    def build_wheels(self) -> None:
        pass
    
    @abstractmethod
    def apply_color(self) -> None:
        pass
    
    @abstractmethod
    def get_result(self) -> Vehicle:
        pass

# Concrete Builders
class CarBuilder(VehicleBuilder):
    def __init__(self):
        self.car = Vehicle()
        self.car.vehicle_type = "Car"
    
    def build_engine(self) -> None:
        self.car.engine = "V6"
    
    def build_chassis(self) -> None:
        self.car.chassis = "Sedan"
    
    def build_wheels(self) -> None:
        self.car.wheels = "4 wheels"
    
    def apply_color(self) -> None:
        self.car.color = RED
    
    def get_result(self) -> Vehicle:
        return self.car

class TruckBuilder(VehicleBuilder):
    def __init__(self):
        self.truck = Vehicle()
        self.truck.vehicle_type = "Truck"
    
    def build_engine(self) -> None:
        self.truck.engine = "V8"
    
    def build_chassis(self) -> None:
        self.truck.chassis = "Pickup"
    
    def build_wheels(self) -> None:
        self.truck.wheels = "6 wheels"
    
    def apply_color(self) -> None:
        self.truck.color = BLUE
    
    def get_result(self) -> Vehicle:
        return self.truck

class MotorcycleBuilder(VehicleBuilder):
    def __init__(self):
        self.motorcycle = Vehicle()
        self.motorcycle.vehicle_type = "Motorcycle"
    
    def build_engine(self) -> None:
        self.motorcycle.engine = "VTwin"
    
    def build_chassis(self) -> None:
        self.motorcycle.chassis = "Sport"
    
    def build_wheels(self) -> None:
        self.motorcycle.wheels = "2 wheels"
    
    def apply_color(self) -> None:
        self.motorcycle.color = YELLOW
    
    def get_result(self) -> Vehicle:
        return self.motorcycle

# Director
class VehicleDirector:
    def __init__(self, builder: VehicleBuilder):
        self.builder = builder
    
    def construct(self) -> None:
        self.builder.build_engine()
        self.builder.build_chassis()
        self.builder.build_wheels()
        self.builder.apply_color()
    
    def change_builder(self, builder: VehicleBuilder) -> None:
        self.builder = builder

# Client
class Game:
    def __init__(self):
        self.vehicles = []
        self.builders = {
            "car": CarBuilder(),
            "truck": TruckBuilder(),
            "motorcycle": MotorcycleBuilder()
        }
        self.director = VehicleDirector(self.builders["car"])

    def create_vehicle(self, vehicle_type: str) -> None:
        if vehicle_type in self.builders:
            self.director.change_builder(self.builders[vehicle_type])
            self.director.construct()
            vehicle = self.director.builder.get_result()
            self.vehicles.append(vehicle)
    
    def display_vehicles(self, screen):
        for i, vehicle in enumerate(self.vehicles):
            position = (200 + i * 200, 200)
            vehicle.display(screen, position)

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

# Main game function
def main():
    game = Game()
    
    # Create buttons
    buttons = [
        Button(100, 50, 150, 50, RED, "Build Car", lambda: game.create_vehicle("car")),
        Button(300, 50, 150, 50, BLUE, "Build Truck", lambda: game.create_vehicle("truck")),
        Button(500, 50, 150, 50, YELLOW, "Build Motorcycle", lambda: game.create_vehicle("motorcycle")),
        Button(300, 500, 150, 50, GREEN, "Reset", lambda: game.vehicles.clear())
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
        screen.fill(WHITE)
        
        # Draw buttons
        for button in buttons:
            button.draw(screen)
        
        # Display vehicles
        game.display_vehicles(screen)
        
        # Draw instructions
        instructions = font.render("Click a button to build a vehicle", True, BLACK)
        screen.blit(instructions, (200, 120))
        
        # Update the display
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
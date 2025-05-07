# Base class
class Animal:
    def speak(self):
        pass

# Concrete classes
class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

# Factory class
class AnimalFactory:
    def create_animal(self, animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError("Unknown animal type")

# Usage
factory = AnimalFactory()

animal1 = factory.create_animal("dog")
animal2 = factory.create_animal("cat")

print(animal1.speak())  # Output: Woof!
print(animal2.speak())  # Output: Meow!

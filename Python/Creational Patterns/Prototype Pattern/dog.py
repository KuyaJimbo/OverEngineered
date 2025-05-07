import copy

# Prototype base class
class Prototype:
    def clone(self):
        return copy.deepcopy(self)

# Concrete class
class Dog(Prototype):
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def __str__(self):
        return f"{self.name} the {self.breed}"

# Usage
original_dog = Dog("Rex", "German Shepherd")
cloned_dog = original_dog.clone()

cloned_dog.name = "Max"

print(original_dog)  # Output: Rex the German Shepherd
print(cloned_dog)    # Output: Max the German Shepherd
print(original_dog is cloned_dog)  # Output: False (different instances)
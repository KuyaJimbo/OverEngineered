# Product
class Burger:
    def __init__(self):
        self.ingredients = []

    def add(self, ingredient):
        self.ingredients.append(ingredient)

    def show(self):
        print("Burger with:", ", ".join(self.ingredients))

# Builder
class BurgerBuilder:
    def __init__(self):
        self.burger = Burger()

    def add_bun(self):
        self.burger.add("bun")
        return self

    def add_patty(self):
        self.burger.add("patty")
        return self

    def add_lettuce(self):
        self.burger.add("lettuce")
        return self

    def add_cheese(self):
        self.burger.add("cheese")
        return self

    def build(self):
        return self.burger

# Director (optional)
class Cook:
    def make_cheeseburger(self):
        return BurgerBuilder().add_bun().add_patty().add_cheese().add_bun().build()

# Usage
cook = Cook()
burger = cook.make_cheeseburger()
burger.show()  # Output: Burger with: bun, patty, cheese, bun

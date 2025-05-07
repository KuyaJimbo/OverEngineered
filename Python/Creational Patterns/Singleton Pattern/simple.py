class Singleton:
    _instance = None

    def __init__(self):
        if Singleton._instance is not None:
            raise Exception("This class is a singleton! Use get_instance() instead.")
        print("Initializing singleton...")
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Singleton()
        return cls._instance

# Usage
s1 = Singleton.get_instance()
s2 = Singleton.get_instance()

print(s1 is s2)  # Output: True
print(s1)  # Output: <__main__.Singleton object at ...>
print(s2)  # Output: <__main__.Singleton object at ...>
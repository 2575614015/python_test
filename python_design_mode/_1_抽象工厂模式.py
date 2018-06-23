import random


class PetShop(object):
    def __init__(self,animal_factory=None):
        #  pet 宠物  factory 工厂
        self.pet_factory = animal_factory

    def show_pet(self):
        pet = self.pet_factory.get_pet()
        print("this is a lovely", pet)
        print("it says",pet.speak())
        print("it eats",self.pet_factory.get_food())


class Dog:
    def speak(self):
        return "Dog"

    def __str__(self):
        return "this is Dog"


class Cat:
    def speak(self):
        return "Cat"

    def __str__(self):
        return "this is Cat"


class CatFactory:
    def get_pet(self):
        return Cat()

    def get_food(self):
        return "cat food"

class DogFactory:
    def get_pet(self):
        return Dog()

    def get_food(self):
        return "dog food"


def get_factory():
    return random.choice([DogFactory,CatFactory])

if __name__ == '__main__':
    shop = PetShop() # pet_factory 默认为None，后面延迟加载

    shop.pet_factory = get_factory()()  #  延迟加载，随机选择一个工厂然后实例出来一个对象给商店
    shop.show_pet()


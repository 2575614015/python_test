import os


class Dog:
    def __init__(self):
        self.name ="Dog"

    def bark(self): # bark ：叫声
        return "woof!"  # woof 低吠声


class Cat:
    def __init__(self):
        self.name = "Cat"

    def meow(self):  # meow 猫叫声
        return "meow"   # meow 猫叫声


class Human:
    def __init__(self):
        self.name = "Human"

    def speak(self):
        return "hello, python"


class Car:
    def __init__(self):
        self.name = "Car"

    def make_noise(self, noise_level):
        return "noise level is {}".format(noise_level)


class Adapter: # adapter 适配器
    def __init__(self,obj,adapted_methods):   # adpted 适应
        self.obj = obj
        self.__dict__.update(adapted_methods)   # self.__dict__是打印对象所有的属性，结果是一个字典 {"kye":value}
        # key对应对象的属性，value对应属性的属性值。这里就相当于把不同类的方法都绑定到Adapter这个类实例化出来的
        # 对象的make_noise 属性上面去，该属性的值对应其他类里面的方法。

    def __getattr__(self, attr):  # 当调用类不存的属性或者方法时，就会触发该魔法方法
        return getattr(self.obj, attr)  # getattr(object,attr [,default])


def main():
    objects = []
    dog = Dog()
    objects.append(Adapter(dog,dict(make_noise=dog.bark)))
    cat = Cat()
    objects.append(Adapter(cat,dict(make_noise=cat.meow)))
    human = Human()
    objects.append(Adapter(human,dict(make_noise=human.speak)))
    car = Car()
    car_noise = lambda : car.make_noise(3)
    objects.append(Adapter(car,dict(make_noise=car_noise)))
    for obj in objects:
        print("A",obj.name,"goes",obj.make_noise())  # 这里 obj.make_noise 就相当于 dog.bark 这些方法，后面加括号代表执行

if __name__ == '__main__':
    # 适配器模式相当于把不同类的相似方法给封装到一个类上面去，这些相似的方法最终有一个相同的名字
    main()



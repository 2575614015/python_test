class Director:  # director 监视
    def __init__(self):
        self.builder = None  # builder建造者

    def construct_building(self):
        self.builder.new_building()
        self.builder.build_floor()
        self.builder.build_size()

    def get_building(self):
        return self.builder.building


class Builder:
    def __init__(self):
        self.building = None

    def new_building(self):
        self.building = Building()


class Building:
    def __init__(self):
        self.floor = None
        self.size = None

    def __repr__(self):   #  和__str__ 魔法方法类似，都是打印对象的时候调用，不过repr更强大
        # repr方法在交互式环境下也能起作用，即交互式环境直接输变量名打印的时候
        # __str__ 只有在print的时候才会触发
        return "Floor:%s | Size: %s" % (self.floor,self.size)


class BuilderHouse(Builder):
    def build_floor(self):
        self.building.floor = "One"

    def build_size(self):
        self.building.size = "Big"


class BuilderFlat(Builder):   # flat 公寓
    def build_floor(self):
        self.building.floor = "More than One"

    def build_size(self):
        self.building.size = "small"


if __name__ == '__main__':
    director = Director()
    director.builder = BuilderHouse()
    director.construct_building()
    building = director.get_building()
    print(building)
    director.builder = BuilderFlat()
    director.construct_building()
    building = director.get_building()
    print(building)
class Borg:
    __shared_state = {}

    def __init__(self):
        self.state = None  # 设置默认值防止报错
        self.__dict__ = self.__shared_state  # 等号，浅拷贝，拷贝引用，
        # 后面实例化的对象的__dict__都是这个字典 __shared_state
        # 因为__shared_state 是类属性，所以只有一份，所有的实例对象共用

    def __str__(self):  # 打印对象的时候自动执行的魔法方法
        return self.state   # self.state动态添加


class YourBorg(Borg):

    def hhh(self):
        print(self.__shared_state)
    pass


if __name__ == '__main__':
    rm1 = Borg()
    rm2 = Borg()
    rm1.state = "Done"
    print("rm1.state:", rm1)   # rm1.state: Done
    print("rm1.state:", rm2)   # rm2.state: Done
    rm2.state = "Running"
    print("rm1.state:", rm1)   # rm1.state: Running
    print("rm2.state:", rm2)   # rm2.state: Running
    print("rm1 id:", id(rm1))   # rm1 id: 41601008
    print("rm2 id:", id(rm2))   # rm2 id: 41601064
    rm3 = YourBorg()     # 继承父类的__init__方法，但是私有属性没有继承。初始化的时候调用了父类的初始化方法
    # 下面2句注释证明上述观点
    # rm3.hhh()
    # print(rm3.__shared_state)
    print("rm3.state:", rm3)    # rm3.state: Running


class Handler:
    def __init__(self):
        self.successor = None

    def add_successor(self,successor):  # successor 后续的事，继承者
        self.successor = successor


class ConcreteHandler1(Handler):
    def handle(self,request):
        if request>0 and request<=10:
            print("concreteHandler1 deal %s"%request)
        elif self.successor is not None:
            self.successor.handle(request)
        else:
            print("no handler can deal with %s"%request)


class ConcreteHandler2(Handler):
    def handle(self,request):
        if request>10 and request<=20:
            print("ConcreteHandler2 deal %s"%request)
        elif self.successor is not None:
            self.successor.handle(request)
        else:
            print("no handler can deal with %s" % request)

class ConcreteHandler3(Handler):
    def handle(self,request):
        if request>20 and request<=30:
            print("ConcreteHandler3 deal %s"%request)
        elif self.successor is not None:
            self.successor.handle(request)
        else:
            print("no handler can deal with %s" % request)


if __name__ == '__main__':
    h1 = ConcreteHandler1()  # 创建处理者1
    h2 = ConcreteHandler2()  # 创建处理者2
    h3 = ConcreteHandler3()  # 创建处理者3
    h1.add_successor(h2)  # 添加h1如果处理不了就让h2去处理
    h2.add_successor(h3)  # 如果h2处理不了就让h3去处理
    requests = [1,3,23,42,34,67,11,22,14,36]
    for request in requests:
        h1.handle(request)






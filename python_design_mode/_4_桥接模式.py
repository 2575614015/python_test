class DrawingAPI1:
    def draw_circle(self, x, y, radius):
        print("API1.circle at {} : {}  ,radius:{}".format(x, y, radius))


class DrawingAPI2:
    def draw_circle(self,x,y,radius):
        print("API2.cirle at {} : {}  ,radius:{}".format(x, y, radius))


class CircleShape:
    def __init__(self,x,y,radius,drawing_api):
        self._x = x
        self._y = y
        self._radius = radius
        self._drawing_api = drawing_api

    def draw(self):
        self._drawing_api.draw_circle(self._x,self._y,self._radius)

    def scale(self,pct):   # scale 规模
        self._radius *= pct   # pct 百分比


def main():
    shapes = (
        CircleShape(1,2,3,DrawingAPI1()),
        CircleShape(5,7,11,DrawingAPI2()),
    )  # 提供2个
    for shape in shapes:
        shape.scale(2.5)
        shape.draw()

if __name__ == '__main__':
    # 桥接模式就是一个类的属性的值是另一个类的实例对象。然后可以通过这个类的实例对象去调用另外一个类对象的方法
    main()
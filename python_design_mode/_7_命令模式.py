import os
class MoveFileCommand(object):
    def __init__(self,src,dest):
        self.src = src
        self.dest = dest

    def execute(self):
        self() # 直接调用对象本身会执行__call__方法

    def __call__(self, *args, **kwargs):  # __call__ 魔法方法直接调用对象的时候执行的方法
        print("renaming {} to {}".format(self.src,self.dest))
        os.rename(self.src,self.dest)

    def undo(self):
        print("renaming {} to {}".format(self.dest,self.src))
        os.rename(self.dest,self.src)


if __name__ == '__main__':
    command_stack = []
    command_stack.append(MoveFileCommand("foo.txt","bar.txt"))
    command_stack.append(MoveFileCommand("bar.txt","foo.txt"))

    for cmd in command_stack:
        cmd.execute()

    for cmd in reversed(command_stack):
        cmd.undo()

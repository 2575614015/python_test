def normalize(val):   # normalize 格式化
    if val.find("-") != -1:
        val = val.replace("-","_")

    return val

def denormalize(val):
    if val.find("_") != -1:
        val = val.replace("_","-")

    return val


class SpecialDict(dict):
    def __getattr__(self, name):  # getattr 魔法方法是在访问不存在的属性时执行的方法
        if name in self.__dict__:
            return self.__dict__[name]
        elif name in self:
            return self.get(name,None)
        else:
            name = denormalize(name)
            if name in self:
                return self.get(name,None)
            else:
                raise AttributeError("no attribute named %s"%name)

    def __setattr__(self, name, value):
        if name in self.__dict__:
            self.__dict__[name] = value
        elif name in self:
            self[name] = value
        else:
            name2 = denormalize(name)
            if name2 in self:
                self[name2] = value
            else:
                self[name] = value


class CompositeDict(SpecialDict):
    ID = 0
    def __init__(self, name= ""):
        if name:
            self.name = name
        else:
            self._name = name.join(("id#",str(self.__class__.ID))) # 对象调用__class__方法是指向实例化自己的类
            self.__class__.ID += 1   # 这里self.__class__.ID 相当于 CompositeDict.ID
        self.children = []
        self._father = None
        self[self._name] = SpecialDict()

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        elif name in self:
            return self.get(name,None)
        else:
            name = denormalize(name)
            if name in self:
                return self.get(name,None)
            else:
                child = self.findChild(name)
                if child:
                    return child
                else:
                    attr = getattr(self[self._name],name)
                    if attr:
                        return attr
                    raise AttributeError("no attribute named %s " % name)

    def isRoot(self):
        return not self._father

    def isLeaf(self):
        return self._children

    def getName(self):
        return self._name

    def getIndex(self,child):
        if child in self._children:
            return self._children.index(child)
        else:
            return -1

    def getDict(self):
        return self[self._name]

    def getProperty(self,child,key):
        childDict = self.getInfoDict(child)
        if childDict:
            return childDict.get(key,None)

    def setProperty(self,child,key,value):
        childDict = self.getInfoDict(child)
        if childDict:
            child[key] = value

    def getChildren(self):
        return self._children

    def getAllChildren(self):
        l = []
        for child in self._children:
            l.append(child)
            l.extend(child.getAllChildren())
        return l

    def getChild(self,name):
        for child in self._children:
            if child.getName() == name:
                return child

    def findChild(self,name):
        for child in self.getAllChildren():
            if child.getName() == name:
                return child

    def findChildren(self,name):
        children = []
        for child in self.getAllChildren():
            if child.getName() == name:
                child.append(child)

        return children

    def getPropertyDict(self):
        """ Return the property dictionary """

        d = self.getChild('__properties')
        if d:
            return d.getDict()
        else:
            return {}

    def getParent(self):
        """ Return the person who created me """

        return self._father

    def __setChildDict(self, child):
        """ Private method to set the dictionary of the child
        object 'child' in the internal dictionary """

        d = self[self._name]
        d[child.getName()] = child.getDict()

    def setParent(self, father):
        """ Set the parent object of myself """

        # This should be ideally called only once
        # by the father when creating the child :-)
        # though it is possible to change parenthood
        # when a new child is adopted in the place
        # of an existing one - in that case the existing
        # child is orphaned - see addChild and addChild2
        # methods !
        self._father = father

    def setName(self, name):
        """ Set the name of this ConfigInfo object to 'name' """

        self._name = name

    def setDict(self, d):
        """ Set the contained dictionary """

        self[self._name] = d.copy()

    def setAttribute(self, name, value):
        """ Set a name value pair in the contained dictionary """

        self[self._name][name] = value

    def getAttribute(self, name):
        """ Return value of an attribute from the contained dictionary """

        return self[self._name][name]

    def addChild(self, name, force=False):
        """ Add a new child 'child' with the name 'name'.
        If the optional flag 'force' is set to True, the
        child object is overwritten if it is already there.

        This function returns the child object, whether
        new or existing """

        if type(name) != str:
            raise ValueError('Argument should be a string!')

        child = self.getChild(name)
        if child:
            # print 'Child %s present!' % name
            # Replace it if force==True
            if force:
                index = self.getIndex(child)
                if index != -1:
                    child = self.__class__(name)
                    self._children[index] = child
                    child.setParent(self)

                    self.__setChildDict(child)
            return child
        else:
            child = self.__class__(name)
            child.setParent(self)

            self._children.append(child)
            self.__setChildDict(child)

            return child

    def addChild2(self, child):
        """ Add the child object 'child'. If it is already present,
        it is overwritten by default """

        currChild = self.getChild(child.getName())
        if currChild:
            index = self.getIndex(currChild)
            if index != -1:
                self._children[index] = child
                child.setParent(self)
                # Unset the existing child's parent
                currChild.setParent(None)
                del currChild

                self.__setChildDict(child)
        else:
            child.setParent(self)
            self._children.append(child)
            self.__setChildDict(child)

if __name__ == "__main__":
    window = CompositeDict('Window')
    frame = window.addChild('Frame')
    tfield = frame.addChild('Text Field')
    tfield.setAttribute('size', '20')

    btn = frame.addChild('Button1')
    btn.setAttribute('label', 'Submit')

    btn = frame.addChild('Button2')
    btn.setAttribute('label', 'Browse')

    # print(window)
    # print(window.Frame)
    # print(window.Frame.Button1)
    # print(window.Frame.Button2)
    print(window.Frame.Button1.label)
    print(window.Frame.Button2.label)





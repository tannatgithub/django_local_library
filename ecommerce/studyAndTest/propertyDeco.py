class Property:
    def __init__(self, var):
        ## initializing the attribute
        self.__a = var

    @property
    def a(self):
        return self.__a

    ## the attribute name and the method name must be same which is used to set the value for the attribute
    # # @a.setter
    # def a(self, var):
    #     if var > 0 and var % 2 == 0:
    #         self.__a = var
    #     else:
    #         self.__a = 2

def test1():
    obj = Property(23)
    print(obj.a)
    # outside = obj.__a
    # print(outside)

if __name__ == "__main__":
    test1()
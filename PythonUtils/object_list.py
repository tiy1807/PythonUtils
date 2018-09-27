# ------------------------------------------------------------------------------
# Class ObjectList
#
# Abstract container for objects. Used in conjunction with Store class.
# object_class should be a class, which has a to_csv method, which converts the
# data into a list. This is data that is used in the constructor.
# ------------------------------------------------------------------------------

class ObjectList:
    def __init__(self, object_class, object_list=[]):
        self.object_list = object_list
        self.object_class = object_class

    def _add(self, *args):
        # *args is a list (or other iterable object) that contains the arguments
        # for the constructor of the object_class.
        self.object_list.append(self.object_class(*args))

    def to_csv(self):
        result = []
        for object in self.object_list:
            result.append(object.to_csv())
        return result

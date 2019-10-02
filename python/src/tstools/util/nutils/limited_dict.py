
__all__ = ["create_struct", "initialize_obj_properties"]

class LimitedDict(dict):

    def __init__(self, update):
        self.update(update)
        self._key_list = list(self.keys())

    def __setitem__(self, key, val):
        if key not in self._key_list:
            raise KeyError

        dict.__setitem__(self, key, val)

def create_struct(inp):
    class LimitedObj:
        if type(inp) == type([]):
            __slots__ = inp

        elif type(inp) == type({}):
            __slots__ = list(inp.keys())

        else:
            print("Non implemented")
            exit(1)

        def __init__(self):
            if type(inp) == type({}):
                for var in inp.keys():
                    self.__setattr__(var, inp[var])

    obj = LimitedObj()

    return obj

def initialize_obj_properties(obj, dictD):
    for key in dictD.keys():
        obj.__setattr__(key, dictD[key])




class UnifiBaseObject(object):
    def __init__(self, controller, raw):
        self.__controller = controller
        self.__raw = raw

    @property
    def controller(self):
        return self.__controller

    def __getattr__(self, name):
        if name not in self.__raw:
            raise ValueError('{type} has no attribute "{name}"'.format(type=self.__class__.__name__, name=name))

        return self.__raw[name]
class Material():
    _repo = {}
    def __init__(self, name, **kwargs):
        self.name = name
        self.__dict__.update(**kwargs)
        self._repo.update({self.name: self})

class Message():
    _repo = []
    def __init__(self, message):
        self.message = message
        self._repo.append(self)





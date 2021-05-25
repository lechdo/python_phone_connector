# encoding:utf-8
from collections import namedtuple
from enum import Enum
from collections import abc
from keyword import iskeyword


class State(Enum):
    NOT_HOME = 0
    HOME = 1


class Phone:
    """
    Représentation des données d'un telephone.

    Le statut étant modifiable, l'objet ne comprend pas de hashing, et a un process de comparaison custom.

    """
    __slots__ = ("__name", "__mac", "status")

    def __init__(self, name, mac, status=State.NOT_HOME):
        self.__name = name
        self.__mac = mac
        self.status = status

    def __repr__(self):
        return f"<Phone(name={self.__name} , mac={self.__mac}, status={self.status})"

    @property
    def name(self):
        return self.__name

    @property
    def mac(self):
        return self.__mac

    def __str__(self):
        return f"<Phone Object : name: {self.__name}, mac: {self.__mac}"

    def __eq__(self, other):
        assert isinstance(other, Phone), "not comparable to another type."
        if other.name == self.name and other.mac == self.mac:
            return True
        return False


Cli = namedtuple('Client', 'name username password certificate_file mqtt_broker port')


class FrozenJson:
    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if iskeyword(key):
                key += '_'
            if not key.isidentifier():
                key = 'v_' + key
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJson(self.__data[name])

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

    def __repr__(self):
        return str(self.__data)

    def __str__(self):
        return self.__repr__()


def singleton(class_):
    instance = None

    def inner(*args, **kwargs):
        nonlocal instance
        if instance:
            if any(args) or any(kwargs):
                raise PermissionError("cannot re-initialize the instance with parameters")
            return instance
        instance = class_(*args, **kwargs)
        return instance

    return inner




@singleton
class Params:
    __slots__ = ("__data", )

    def __init__(self, data=None):
        self.__data = FrozenJson(data)

    def __getattr__(self, item):
        return getattr(self.__data, item)

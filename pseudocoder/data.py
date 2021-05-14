# contains class definition for anything and everything that goes in a slot
from typing import Type, Any
from pseudocoder import interfaces


# for containing builtin data types
class BuiltInDataType(interfaces.DataType):
    def __init__(self, data_type: Type[interfaces.data]):
        self.__data_type = data_type

    def is_type(self, *args) -> bool:
        if len(args) == 0:
            return isinstance(self, BuiltInDataType)
        else:
            return isinstance(args[0], self.__data_type)

    def from_python(self, val) -> interfaces.data:
        return self.__data_type(val)


class String(interfaces.data):
    def __init__(self, string: str) -> None:
        self.__string = string

    def to_python(self) -> str:
        return self.__string


class Char(interfaces.data):
    def __init__(self, char: str):
        assert len(char) == 1
        self.__char = char

    def to_python(self) -> str:
        return self.__char


class Real(interfaces.number[float]):
    def __init__(self, num) -> None:
        super(Real, self).__init__(float(num))


class Integer(interfaces.number[int]):
    def __init__(self, num) -> None:
        super(Integer, self).__init__(round(num))


class Boolean(interfaces.data):
    def __init__(self, truth: bool):
        self.__truth = truth

    def to_python(self) -> bool:
        return self.__truth


class Date(interfaces.data):
    def __init__(self, year, month, day) -> None:
        assert 0 < day <= 31
        assert 0 < month <= 12
        assert year > 1973

        self.__year, self.__month, self.__day = year, month, day

    def to_python(self) -> tuple:
        return self.__year, self.__month, self.__day


class UserDefinedCompositeType:  # TODO
    ...


class UserDefinedEnumerableType:  # TODO
    ...


class UserDefinedPointerType:  # TODO
    ...


class UserDefinedComposite(interfaces.data):  # TODO
    ...

    @classmethod
    def declare_variable(cls, identifier: str, datatype: Type[interfaces.data]):
        pass


class UserDefinedEnumerable(interfaces.data):  # TODO
    ...


class UserDefinedPointer(interfaces.data):  # TODO
    ...

# Contains all the operations: things that are evaluated to get a value, and not executed to get a result.
from pseudocoder import interfaces
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pseudocoder.namespaces import NameSpace
    from pseudocoder import data


class Addition(interfaces.evaluable):
    def __init__(self, _a: interfaces.evaluable, _b: interfaces.evaluable) -> None:
        self.__a = _a
        self.__b = _b

    def evaluate(self, namespace: 'NameSpace') -> interfaces.number:
        a = self.__a.evaluate(namespace)
        b = self.__b.evaluate(namespace)
        assert isinstance(a, interfaces.number)
        assert isinstance(b, interfaces.number)
        a = a.to_python()
        b = b.to_python()
        c = a + b
        if isinstance(c, float):
            return self.get_type('REAL', namespace).from_python(c)
        else:
            return self.get_type('INTEGER', namespace).from_python(c)


class Subtraction(interfaces.evaluable):
    def __init__(self, _a: interfaces.evaluable, _b: interfaces.evaluable) -> None:
        self.__a = _a
        self.__b = _b

    def evaluate(self, namespace: 'NameSpace') -> interfaces.number:
        a = self.__a.evaluate(namespace)
        b = self.__b.evaluate(namespace)
        assert isinstance(a, interfaces.number)
        assert isinstance(b, interfaces.number)
        a = a.to_python()
        b = b.to_python()
        c = a - b
        if isinstance(c, float):
            return self.get_type('REAL', namespace).from_python(c)
        else:
            return self.get_type('INTEGER', namespace).from_python(c)


class Multiplication(interfaces.evaluable):
    def __init__(self, _a: interfaces.evaluable, _b: interfaces.evaluable) -> None:
        self.__a = _a
        self.__b = _b

    def evaluate(self, namespace: 'NameSpace') -> interfaces.number:
        a = self.__a.evaluate(namespace)
        b = self.__b.evaluate(namespace)
        assert isinstance(a, interfaces.number)
        assert isinstance(b, interfaces.number)
        a = a.to_python()
        b = b.to_python()
        c = a * b
        if isinstance(c, float):
            return self.get_type('REAL', namespace)(c)
        else:
            return self.get_type('INTEGER', namespace)(c)


class Division(interfaces.evaluable):
    def __init__(self, _a: interfaces.evaluable, _b: interfaces.evaluable) -> None:
        self.__a = _a
        self.__b = _b

    def evaluate(self, namespace: 'NameSpace') -> 'data.Real':
        a = self.__a.evaluate(namespace)
        b = self.__b.evaluate(namespace)
        assert isinstance(a, interfaces.number)
        assert isinstance(b, interfaces.number)
        a = a.to_python()
        b = b.to_python()
        c = a / b
        return self.get_type('REAL', namespace)(c)


class Concatenation(interfaces.evaluable):
    def __init__(self, _a: interfaces.evaluable, _b: interfaces.evaluable) -> None:
        self.__a = _a
        self.__b = _b

    def evaluate(self, namespace: 'NameSpace') -> 'data.String':
        a = self.__a.evaluate(namespace)
        b = self.__b.evaluate(namespace)
        assert isinstance(a, self.get_type('STRING', namespace)) or isinstance(a, self.get_type('CHAR', namespace))
        assert isinstance(b, self.get_type('STRING', namespace)) or isinstance(a, self.get_type('CHAR', namespace))
        a = a.to_python()
        b = b.to_python()
        c = a + b
        return self.get_type('STRING', namespace)(c)


class GreaterThan(interfaces.evaluable):
    def __init__(self, _a: interfaces.evaluable, _b: interfaces.evaluable) -> None:
        self.__a = _a
        self.__b = _b

    def evaluate(self, namespace: 'NameSpace') -> 'data.Boolean':
        a = self.__a.evaluate(namespace)
        b = self.__b.evaluate(namespace)
        assert isinstance(a, interfaces.number)
        assert isinstance(b, interfaces.number)
        a = a.to_python()
        b = b.to_python()
        c = a > b
        return self.get_type('BOOLEAN', namespace)(c)


class LessThan(interfaces.evaluable):
    def __init__(self, _a: interfaces.evaluable, _b: interfaces.evaluable) -> None:
        self.__a = _a
        self.__b = _b

    def evaluate(self, namespace: 'NameSpace') -> 'data.Boolean':
        a = self.__a.evaluate(namespace)
        b = self.__b.evaluate(namespace)
        assert isinstance(a, interfaces.number)
        assert isinstance(b, interfaces.number)
        a = a.to_python()
        b = b.to_python()
        c = a < b
        return self.get_type('BOOLEAN', namespace)(c)


class GreaterThanEqual(interfaces.evaluable):
    def __init__(self, _a: interfaces.evaluable, _b: interfaces.evaluable) -> None:
        self.__a = _a
        self.__b = _b

    def evaluate(self, namespace: 'NameSpace') -> 'data.Boolean':
        a = self.__a.evaluate(namespace)
        b = self.__b.evaluate(namespace)
        assert isinstance(a, interfaces.number)
        assert isinstance(b, interfaces.number)
        a = a.to_python()
        b = b.to_python()
        c = a >= b
        return self.get_type('BOOLEAN', namespace)(c)


class LessThanEqual(interfaces.evaluable):
    def __init__(self, _a: interfaces.evaluable, _b: interfaces.evaluable) -> None:
        self.__a = _a
        self.__b = _b

    def evaluate(self, namespace: 'NameSpace') -> 'data.Boolean':
        a = self.__a.evaluate(namespace)
        b = self.__b.evaluate(namespace)
        assert isinstance(a, interfaces.number)
        assert isinstance(b, interfaces.number)
        a = a.to_python()
        b = b.to_python()
        c = a <= b
        return self.get_type('BOOLEAN', namespace)(c)


class Equal(interfaces.evaluable):
    def __init__(self, _a: interfaces.evaluable, _b: interfaces.evaluable) -> None:
        self.__a = _a
        self.__b = _b

    def evaluate(self, namespace: 'NameSpace') -> 'data.Boolean':
        a = self.__a.evaluate(namespace)
        b = self.__b.evaluate(namespace)
        assert (isinstance(a, interfaces.number) and isinstance(b, interfaces.number)) or \
               (isinstance(a, self.get_type('STRING', namespace)) and isinstance(b, self.get_type('STRING', namespace))) or \
               (isinstance(a, self.get_type('CHAR', namespace)) and isinstance(b, self.get_type('CHAR', namespace)))
        a = a.to_python()
        b = b.to_python()
        c = a == b
        return self.get_type('BOOLEAN', namespace)(c)


class NotEqual(interfaces.evaluable):
    def __init__(self, _a: interfaces.evaluable, _b: interfaces.evaluable) -> None:
        self.__a = _a
        self.__b = _b

    def evaluate(self, namespace: 'NameSpace') -> 'data.Boolean':
        a = self.__a.evaluate(namespace)
        b = self.__b.evaluate(namespace)
        a = a.to_python()
        b = b.to_python()
        c = a != b
        return self.get_type('BOOLEAN', namespace).to_python(c)


class Identifier(interfaces.evaluable):
    def __init__(self, _id) -> None:
        self.__id = _id

    def evaluate(self, namespace: 'NameSpace') -> interfaces.data:
        return namespace.lookup(self.__id)

    def get_identifier(self) -> str:
        return self.__id


class StringLiteral(interfaces.evaluable):
    def __init__(self, string: str) -> None:
        self.__string = string

    def evaluate(self, namespace: 'NameSpace') -> 'data.String':
        return self.get_type('STRING', namespace).from_python(self.__string)


class CharLiteral(interfaces.evaluable):
    def __init__(self, char: str) -> None:
        assert len(char) == 1
        self.__char = char

    def evaluate(self, namespace: 'NameSpace') -> 'data.Char':
        return self.get_type('CHAR', namespace).from_python(self.__char)


class IntegerLiteral(interfaces.evaluable):
    def __init__(self, integer: int):
        self.__integer = integer

    def evaluate(self, namespace: 'NameSpace') -> 'data.Integer':
        return self.get_type('INTEGER', namespace).from_python(self.__integer)


class RealLiteral(interfaces.evaluable):
    def __init__(self, real: float):
        self.__real = real

    def evaluate(self, namespace: 'NameSpace') -> 'data.Real':
        return self.get_type('REAL', namespace).from_python(self.__real)


class BooleanLiteral(interfaces.evaluable):
    def __init__(self, boolean: bool):
        self.__boolean = boolean

    def evaluate(self, namespace: 'NameSpace') -> 'data.Boolean':
        return self.get_type('BOOLEAN', namespace).from_python(self.__boolean)


class FunctionEvaluate(interfaces.evaluable):
    def __init__(self, function_name: str, *arguments: str):
        self.__name = function_name
        self.__args = arguments

    def evaluate(self, namespace: 'NameSpace') -> interfaces.data:
        function = namespace.lookup(self.__name)
        assert isinstance(function, interfaces.Function)
        return function.run(namespace, *self.__args)

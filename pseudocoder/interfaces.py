from __future__ import annotations
# Contains the abstract base classes and other miscelaneous classes that are in this file because they are often used
# for type hinting. This is the 'root' python file in that it is imported by nearly ever other python file,
# and itself imports none of them.
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from namespaces import Parameters, FunctionNameSpace, NameSpace


class instruction(ABC):
    @abstractmethod
    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None: ...


class data(ABC):
    @abstractmethod
    def __init__(self, val: Any): raise NotImplementedError()

    def to_python(self) -> Any:
        raise TypeError("This type has no python analogue coded")


N = TypeVar('N', int, float)


class number(data, Generic[N]):
    def __init__(self, num: N):
        self.__num = num

    def to_python(self) -> N:
        return self.__num


class evaluable(ABC):
    @abstractmethod
    def evaluate(self, namespace: 'NameSpace') -> data:
        ...

    @staticmethod
    def get_type(type_name, namespace: 'NameSpace') -> 'DataType':
        type_obj = namespace.lookup(type_name)
        assert isinstance(type_obj, DataType)
        return type_obj


class FunctionEnd(Exception):
    def __init__(self, value: data) -> None:
        self.value = data
        super(FunctionEnd, self).__init__("The RETURN keyword was invoked outside of a function")


class DataType(data, ABC):
    @abstractmethod
    def is_type(self, obj) -> bool: ...  # allows functions to check for pseudocode instances of data types by
    # retrieving the container from the namespace. A previous solution using python's isinstance and meta-types
    # collapsed into spaghetti code and mysterious errors.

    def from_python(self, v):
        raise NotImplementedError()


class Procedure(data):
    def to_python(self) -> Any:
        super(Procedure, self).to_python()

    def __init__(
            self,
            params: 'Parameters',
            instructions: tuple[instruction, ...],
            parent: 'NameSpace'
    ) -> None:
        self.__params = params
        self.__instructions = instructions
        self.__parent = parent

    def run(self, namespace: 'NameSpace', *arguments: evaluable):
        proc_namespace = FunctionNameSpace(self.__parent)
        self.__params.pass_parameters(arguments, namespace, proc_namespace)
        for instruction in self.__instructions:
            instruction.execute(proc_namespace, proc_namespace)


class Function(Procedure):
    def to_python(self) -> Any:
        super(Function, self).to_python()

    def __init__(
            self,
            params: Parameters,
            return_type: DataType,
            instructions: tuple[instruction, ...],
            parent: 'NameSpace'
    ) -> None:
        super(Function, self).__init__(params, instructions, parent)
        self.__return_type = return_type

    def run(self, namespace: 'NameSpace', *arguments: evaluable):
        try:
            super(Function, self).run(namespace, *arguments)
        except FunctionEnd as e:
            assert self.__return_type.is_type(e.value)
            return e.value
        else:
            raise Exception("Function failed to return")

# for defining namespaces and the slots that allow the passing of references to variables
from typing import TypeVar, Generic, TYPE_CHECKING, Type, Union

from pseudocoder import interfaces
from pseudocoder.data import BuiltInDataType, Real, Integer, Boolean
from pseudocoder import operations
from pseudocoder.interfaces import data

if TYPE_CHECKING:
    pass

SomeData = TypeVar('SomeData', bound=interfaces.data)


# slots were implemented to allow the passing of references variables between namespaces. The same slot could occupy
# a variable name in both namespaces. A data type that itself contains a slot could be used to implement pointers.
class Slot(Generic[SomeData]):
    def __init__(self, slot_type: Union[Type[interfaces.DataType], interfaces.DataType]) -> None:
        self.__stored = None
        self.__type = slot_type

    def set(self, value: SomeData) -> None:
        assert self.__type.is_type(value)
        self.__stored = value

    def get(self) -> SomeData:
        if self.__stored is None:
            raise Exception('Not Yet Set')
        else:
            return self.__stored


class NameSpace:

    def __init__(self, parent: 'Optional[NameSpace]' = None) -> None:
        self._variables: dict[str, Slot] = dict()
        self._constants: dict[str, data] = dict()
        self._parent = parent

    def lookup(self, identifier: str) -> data:
        if identifier in self._variables:
            return self._variables[identifier].get()
        elif identifier in self._constants:
            return self._constants[identifier]
        elif self._parent is not None:
            return self._parent.lookup(identifier)
        else:
            raise AssertionError(f'{identifier} is not found in this namespace.')

    def lookup_variable(self, identifier: str) -> Slot:
        if identifier in self._variables:
            return self._variables[identifier]
        elif self._parent is not None:
            return self._parent.lookup_variable(identifier)
        else:
            raise AssertionError(f'Variable {identifier} is not found in this namespace.')

    def lookup_constant(self, identifier: str) -> data:
        if identifier in self._constants:
            return self._constants[identifier]
        elif self._parent is not None:
            return self._parent.lookup_constant(identifier)
        else:
            raise AssertionError(f'Constant {identifier} is not found in this namespace.')

    def declare_variable(self, identifier: str, datatype: 'DataType'):
        if identifier not in self._variables and identifier not in self._constants:
            self._variables[identifier] = Slot(datatype)
        else:
            raise AssertionError(f'{identifier} is already defined.')

    def declare_constant(self, identifier: str, datatype: 'DataType', value: data):
        if identifier not in self._variables and identifier not in self._constants:
            assert datatype.is_type(value)
            self._constants[identifier] = value
        else:
            raise AssertionError(f'{identifier} is already defined.')


class FunctionNameSpace(NameSpace):
    def pass_reference(self, identifier: str, slot: Slot):
        self._variables[identifier] = slot

    def pass_value(self, identifier: str, data_type: interfaces.DataType, value: interfaces.data):
        self.declare_variable(identifier, data_type)
        self.lookup_variable(identifier).set(value)


class Parameters:
    def __init__(self) -> None:
        self.__params: list[tuple[str, interfaces.DataType, bool]] = []

    def add_parameter(self, identifier: str, type_name: str, type_namespace: NameSpace, by_ref: bool) -> None:
        data_type = type_namespace.lookup(type_name)
        assert isinstance(data_type, interfaces.DataType)
        self.__params.append((identifier, data_type, by_ref))

    def pass_parameters(
            self,
            identifiers: tuple[interfaces.evaluable],
            outside_namespace: NameSpace,
            inside_namespace: FunctionNameSpace
    ) -> None:

        assert len(self.__params) == len(identifiers)
        for outside_identifier, param in zip(identifiers, self.__params):
            inside_identifier, data_type, by_ref = param
            if by_ref:
                assert isinstance(outside_identifier, operations.Identifier)
                outside_identifier = outside_identifier.get_identifier()
                slot = outside_namespace.lookup_variable(outside_identifier)
                assert data_type.is_type(slot.get())
                inside_namespace.pass_reference(inside_identifier, slot)
            else:
                data_value = outside_identifier.evaluate(outside_namespace)
                assert data_type.is_type(data_value)
                inside_namespace.pass_value(inside_identifier, data_type, data_value)


# The global namespace defines on initialisation the built in types that can be used. At the moment only the built in
# types supported by the ast converter are used. Since every namespace bar should find the global on a an eventual
# parent, this is the only place where this need to happen
class GlobalNameSpace(NameSpace):

    def __init__(self) -> None:
        super(GlobalNameSpace, self).__init__()
        builtins = {
            'REAL': BuiltInDataType(Real),
            'INTEGER': BuiltInDataType(Integer),
            'BOOLEAN': BuiltInDataType(Boolean),
        }
        self._constants.update(builtins)

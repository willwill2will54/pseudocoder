# Contains all the instruction: things that are run to get a value, and not executed to get a result.
from pseudocoder import interfaces
from pseudocoder import data
from typing import TYPE_CHECKING

from pseudocoder.interfaces import FunctionEnd, evaluable
from pseudocoder.namespaces import NameSpace
from pseudocoder.operations import Identifier

if TYPE_CHECKING:
    pass


class ProcedureCall(interfaces.instruction):
    def __init__(self, procedure_name: str, *arguments: str):
        self.__name = procedure_name
        self.__args = arguments

    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        procedure = lookup_namespace.lookup(self.__name)
        assert isinstance(procedure, interfaces.Function)
        return procedure.run(lookup_namespace, *self.__args)


class VariableDeclaration(interfaces.instruction):
    def __init__(self, identifier: Identifier, type_identifier: evaluable) -> None:
        self.__id = identifier
        self.__type = type_identifier

    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        data_type = self.__type.evaluate(lookup_namespace)
        assert isinstance(data_type, interfaces.DataType)
        action_namespace.declare_variable(self.__id.get_identifier(), data_type)


class ConstantDeclaration(interfaces.instruction):

    def __init__(self, identifier: str, type_identifier: str, value: interfaces.evaluable) -> None:
        self.__id = identifier
        self.__type = type_identifier
        self.__value = value

    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        data_type = lookup_namespace.lookup(self.__type)
        assert isinstance(data_type, interfaces.DataType)
        data_value = self.__value.evaluate(lookup_namespace)
        assert data_type.is_type(data_value)
        action_namespace.declare_constant(self.__id, data_type, data_value)


class CompositeTypeDeclaration(interfaces.instruction):  # TODO
    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        pass


class EnumeratedTypeDeclaration(interfaces.instruction):  # TODO
    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        pass


class PointerTypeDeclaration(interfaces.instruction):  # TODO
    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        pass


class VariableAssignment(interfaces.instruction):
    def __init__(self, identifier: Identifier, value: interfaces.evaluable):
        self.__id = identifier
        self.__value = value

    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        data_value = self.__value.evaluate(lookup_namespace)
        slot = action_namespace.lookup_variable(self.__id.get_identifier())
        slot.set(data_value)


class FunctionReturn(interfaces.instruction):
    def __init__(self, returned: interfaces.evaluable):
        self.__value = returned

    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        data_value = self.__value.evaluate(lookup_namespace)
        raise FunctionEnd(data_value)


class Input(interfaces.instruction): # TODO
    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        pass


class Output(interfaces.instruction):
    def __init__(self, output: interfaces.evaluable):
        self.__out = output

    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        data_value = self.__out.evaluate(lookup_namespace)
        print(str(data_value.to_python()))


class ForLoop(interfaces.instruction):
    def __init__(
            self, identifier: Identifier,
            from_expression: interfaces.evaluable,
            to_expression: interfaces.evaluable,
            step_expression: interfaces.evaluable,
            instructions: tuple[interfaces.instruction, ...]
    ):
        self.__from = from_expression
        self.__to = to_expression
        self.__instructions = instructions
        self.__id = identifier
        self.__step = step_expression

    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        frm = self.__from.evaluate(lookup_namespace)
        to = self.__to.evaluate(lookup_namespace)
        step = self.__step.evaluate(lookup_namespace)
        integer = lookup_namespace.lookup('INTEGER')
        assert isinstance(integer, interfaces.DataType)
        assert all(integer.is_type(x) for x in (frm, to, step))
        slot = action_namespace.lookup_variable(self.__id.get_identifier())
        for x in range(frm.to_python(), to.to_python() + 1, step.to_python()):
            slot.set(integer.from_python(x))
            for instruction in self.__instructions:
                instruction.execute(lookup_namespace, action_namespace)


class WhileLoop(interfaces.instruction):
    def __init__(self, condition: interfaces.evaluable, instructions: tuple[interfaces.instruction, ...]):
        self.__condition = condition
        self.__instructions = instructions

    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        while True:
            run = self.__condition.evaluate(lookup_namespace)
            assert isinstance(run, data.Boolean)
            if run.to_python():
                for instruction in self.__instructions:
                    instruction.execute(lookup_namespace, action_namespace)
            else:
                break


class DoWhileLoop(WhileLoop):
    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        while True:
            for instruction in self.__instructions:
                instruction.execute(lookup_namespace, action_namespace)
            run = self.__condition.evaluate(lookup_namespace)
            assert isinstance(run, data.Boolean)
            if not run.to_python():
                break


class IfElse(interfaces.instruction):
    def __init__(
        self,
        condition: interfaces.evaluable,
        true_code: tuple[interfaces.instruction, ...],
        false_code: tuple[interfaces.instruction, ...]
    ):
        self.__condition = condition
        self.__code = {True: true_code, False: false_code}

    def execute(self, lookup_namespace: 'NameSpace', action_namespace: 'NameSpace') -> None:
        cond = self.__condition.evaluate(lookup_namespace)
        assert isinstance(cond, data.Boolean)
        for instruction in self.__code[cond.to_python()]:
            instruction.execute(lookup_namespace, action_namespace)

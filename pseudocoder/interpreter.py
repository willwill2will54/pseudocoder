# contains custom semantic analysis code

from pseudocoder.tatsu_gen import PseudoCodeSemantics, PseudoCodeParser, KEYWORDS
from pseudocoder.interfaces import instruction, evaluable
from pseudocoder.operations import Identifier, IntegerLiteral, RealLiteral, Multiplication, Division, Addition
from pseudocoder.operations import Subtraction, Equal, NotEqual, LessThanEqual, GreaterThanEqual, LessThan, GreaterThan
from pseudocoder.instructions import VariableDeclaration, VariableAssignment, ForLoop, IfElse, Output


class CustomSemantics(PseudoCodeSemantics):

    # declare = 'DECLARE' identifier ':' expression;
    def declare(self, ast) -> VariableDeclaration:
        return VariableDeclaration(ast[1], ast[3])

    # identifier = /[A-Za-z_]\w*/ ;
    def identifier(self, ast) -> Identifier:
        return Identifier(ast)

    # product = product '*' product | product '/' product | factor;
    def product(self, ast) -> evaluable:
        if isinstance(ast, tuple) and len(ast) == 3:
            term1, op, term2 = ast
            if op == '*':
                return Multiplication(term1, term2)
            else:
                return Division(term1, term2)
        else:
            return ast

    # product = product '*' product | product '/' product | factor;
    def summing(self, ast) -> evaluable:
        if isinstance(ast, tuple) and len(ast) == 3:
            term1, op, term2 = ast
            if op == '+':
                return Addition(term1, term2)
            else:
                return Subtraction(term1, term2)
        else:
            return ast

    # non_arithmetic_expression =
    #     '(' expression ')' |
    #     boolean_expression |
    #     literal |
    #     identifier ;
    def non_arithmetic_expression(self, ast) -> evaluable:
        if isinstance(ast, tuple):
            if len(ast) == 3 and ast[0] == '(' and ast[2] == ')':
                return ast[1]
            else:
                return ast[0]
        else:
            return ast

    # integer_literal = /[1-9]\d*/ | '0' ;
    def integer_literal(self, ast) -> IntegerLiteral:
        return IntegerLiteral(int(ast))

    # real_literal = /\d+.\d*/;
    def real_literal(self, ast) -> RealLiteral:
        return RealLiteral(float(ast))

    # assignment = identifier assign expression;
    def assignment(self, ast) -> VariableAssignment:
        return VariableAssignment(ast[0], ast[2])

    # if = 'IF' expression 'THEN' instructions ['ELSE' instructions] 'ENDIF' ;
    def if_(self, ast) -> IfElse:
        if len(ast) == 5:
            _, condition, _, then, _ = ast
            return IfElse(condition, tuple(then), ())
        else:
            assert len(ast) == 7
            _, condition, _, then, _, else_, _ = ast
            return IfElse(condition, tuple(then), tuple(else_))

    # for = 'FOR' identifier assign expression 'TO' expression ['STEP' expression] instructions 'ENDFOR';
    def for_(self, ast) -> ForLoop:
        if len(ast) == 8:
            _, ident, _, from_, _, to, code, _ = ast
            return ForLoop(ident, from_, to, IntegerLiteral(1), code)
        else:
            assert len(ast) == 10
            _, ident, _, from_, _, to, _, step, code, _ = ast
            return ForLoop(ident, from_, to, step, code)

    # equal_to = expression '=' expression;
    def equal_to(self, ast) -> Equal:
        return Equal(ast[0], ast[2])

    # not_equal_to = expression '<>' expression;
    def not_equal_to(self, ast) -> NotEqual:
        return NotEqual(ast[0], ast[2])

    # less_than = expression '<' expression;
    def less_than(self, ast) -> LessThan:
        return LessThan(ast[0], ast[2])

    # greater_than = expression '>' expression;
    def greater_than(self, ast) -> GreaterThan:
        return GreaterThan(ast[0], ast[2])

    # less_than_or_equal_to = expression '<=' expression;
    def less_than_or_equal_to(self, ast) -> LessThanEqual:
        return LessThanEqual(ast[0], ast[2])

    # greater_than_or_equal_to = expression '>=' expression;
    def greater_than_or_equal_to(self, ast) -> GreaterThanEqual:
        return GreaterThanEqual(ast[0], ast[2])

    # output = 'OUTPUT' expression;
    def output(self, ast) -> Output:
        return Output(ast[1])


def parse_program(code: str, filename: str = None) -> list[instruction]:
    parser = PseudoCodeParser(keywords=KEYWORDS)

    ast: list[instruction] = parser.parse(
        code,
        rule_name='program',
        filename=filename,
        semantics=CustomSemantics()
    )

    return ast


# for testing the ast converter
if __name__ == '__main__':
    test_code = """
    DECLARE five : INTEGER
    DECLARE stuff : INTEGER

    stuff <- 55

    IF thing THEN
        five <- stuff
    ELSE
        five <- (2 + 5) * 8 - 3 / 4
    ENDIF
    """
    parse_program(test_code)

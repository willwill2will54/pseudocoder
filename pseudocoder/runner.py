from pseudocoder.interpreter import parse_program
from pseudocoder.namespaces import GlobalNameSpace


def run(file: str) -> None:
    with open(file, 'r') as fh:
        code = fh.read()
    ast = parse_program(code, file)
    gn = GlobalNameSpace()
    for instruction in ast:
        instruction.execute(gn, gn)

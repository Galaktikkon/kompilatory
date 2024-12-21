import sys
from parser import Mparser
from scanner import Scanner
from TypeChecker import TypeChecker
from TreePrinter import TreePrinter

if __name__ == "__main__":

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples//opers.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    scanner: Scanner = Scanner()
    text: str = file.read()

    tokens = scanner.tokenize(text)

    if scanner.error_list:
        for error in scanner.error_list:
            print(error)
        raise Exception("Scanner: Found illegal characters")

    parser = Mparser()

    ast = parser.parse(tokens)
    if parser.error_list:
        for error in parser.error_list:
            print(error)
        raise Exception("Parser: Parsing error")

    # ast.print_tree()

    typeChecker = TypeChecker()

    typeChecker.visit(ast)
    if typeChecker.error_list:
        # print(typeChecker.symbol_table)
        for error in typeChecker.error_list:
            print(error)
        raise Exception("TypeChecker: Type error")

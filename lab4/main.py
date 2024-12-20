import sys
from parser import Mparser
from scanner import Scanner
from TypeChecker import TypeChecker
from TreePrinter import TreePrinter

if __name__ == "__main__":

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples//init.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    scanner = Scanner()
    parser = Mparser()

    text = file.read()

    tokens = scanner.tokenize(text)

    ast = parser.parse(tokens)

    # ast.print_tree()

    # Below code shows how to use visitor

    typeChecker = TypeChecker()
    typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)

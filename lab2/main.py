import sys
from scanner import Scanner
from parser import Mparser


if __name__ == "__main__":

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples\\example1.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    parser = Mparser()

    parser.parse(lexer.tokenize(text))

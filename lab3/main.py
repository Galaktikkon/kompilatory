import sys
import os
from scanner import Scanner
from parser import Mparser
from TreePrinter import TreePrinter


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

    ast = parser.parse(lexer.tokenize(text))
    try:
        ast.print_tree()
    except:
        pass
    try:
        cwd = os.getcwd()
        path = os.path.join(cwd, "results")

        if not os.path.isdir(path):
            os.mkdir(path)

        save_file = os.path.join(
            path, str(os.path.basename(filename).split(".")[0] + ".tree.txt")
        )
        print(save_file)
        with open(save_file, "w+") as f:

            sys.stdout = f

            try:
                ast.print_tree()
            except:
                pass
    except IOError:
        sys.exit(0)
    finally:
        sys.stdout = sys.__stdout__

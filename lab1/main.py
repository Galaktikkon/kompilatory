import sys
from sly import Lexer


class Scanner(Lexer):

    tokens = {ID, PLUS, MINUS, MUL, DIV, MAT_PLUS,
              MAT_MINUS, MAT_MUL, MAT_DIV, ASSIGN,
              ADD_ASSIGN, SUB_ASSIGN, MUL_ASSIGN,
              DIV_ASSIGN, LESS, GREATER, LEQ, GEQ,
              NEQ, EQ, OP_BRAC, CL_BRAC, OP_SQ_BRAC,
              CL_SQ_BRAC, OP_CRL_BRAC, CL_CRL_BRAC,
              RANGE, TRANSPOSE, COMMA, SEMICOLON, BREAK,
              CONTINUE, RETURN, EYE, ZEROS, ONES, PRINT,
              INT, FLOAT, STR
              }

    pass


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()

    for tok in lexer.tokenize(text):
        print(tok)

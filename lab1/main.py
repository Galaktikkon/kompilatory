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
              FLOAT, INT, STR
              }

    ignore = ' \t'
    ignore_comment = r'\#.*'
    ignore_newline = r'\n+'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    PLUS = r'\+'
    MINUS = r'-'
    MUL = r'\*'
    DIV = r'/'

    MAT_PLUS = r'.\+'
    MAT_MINUS = r'.-'
    MAT_MUL = r'.\*'
    MAT_DIV = r'./'

    ASSIGN = r'='
    ADD_ASSIGN = r'\+='
    SUB_ASSIGN = r'-='
    MUL_ASSIGN = r'\*='
    DIV_ASSIGN = r'/='

    LESS = r'<'
    GREATER = r'>'
    LEQ = r'<='
    GEQ = r'>='
    NEQ = r'!='
    EQ = r'=='

    OP_BRAC = r'\('
    CL_BRAC = r'\)'
    OP_SQ_BRAC = r'\['
    CL_SQ_BRAC = r'\]'
    OP_CRL_BRAC = r'\{'
    CL_CRL_BRAC = r'\}'
    RANGE = r':'
    TRANSPOSE = r'\''
    COMMA = r','
    SEMICOLON = ';'

    INT = r'\d+'
    



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

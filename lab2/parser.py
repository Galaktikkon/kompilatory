from sly import Parser
from scanner import Scanner

# rekursja prawostronna
# obliczenia robić poziomami (dodawanie liczbowe i dodawanie macierzowe w jednym priorytecie)


class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = "parser.out"

    precedence = (
        ("nonassoc", "=", ADD_ASSIGN, SUB_ASSIGN, MUL_ASSIGN, DIV_ASSIGN),
        ("nonassoc", EQ, NEQ, LEQ, GEQ, ">", "<"),
        ("left", "+", "-", MAT_PLUS, MAT_MINUS),
        ("left", "*", "/", MAT_MUL, MAT_DIV),
        ("right", UMINUS),
        ("left", IFX),
        ("right", ELSE),
    )

    @_("lines line", "line")
    def lines(self, p):
        pass

    @_('PRINT expr ";"', 'RETURN expr ";"')
    def line(self, p):
        pass

    @_('BREAK ";"', 'CONTINUE ";"')
    def line(self, p):
        pass

    @_(
        'lvalue "=" expr ";"',
        'lvalue ADD_ASSIGN expr ";"',
        'lvalue SUB_ASSIGN expr ";"',
        'lvalue MUL_ASSIGN expr ";"',
        'lvalue DIV_ASSIGN expr ";"',
    )
    def line(self, p):
        pass

    @_(
        'IFX "(" condition ")" line ELSE line %prec IFX',
        'IFX "(" condition ")" line %prec ELSE',
    )
    def line(self, p):
        pass

    @_(
        "expr EQ expr",
        "expr NEQ expr",
        "expr LEQ expr",
        "expr GEQ expr",
        'expr "<" expr',
        'expr ">" expr',
    )
    def condition(self, p):
        pass

    @_('FOR ID "=" enumerable ":" enumerable line', 'WHILE "(" condition ")" line')
    def line(self, p):
        pass

    @_(
        'expr "+" expr',
        'expr "-" expr',
        "expr MAT_PLUS expr",
        "expr MAT_MINUS expr",
        'expr "*" expr',
        'expr "/" expr',
        "expr MAT_MUL expr",
        "expr MAT_DIV expr",
    )
    def expr(self, p):
        pass

    @_("vector")
    def expr(self, p):
        pass

    @_("element", 'vector "," element')
    def vector(self, p):
        pass

    @_('ZEROS "(" enumerable ")"', 'EYE "(" enumerable ")"', 'ONES "(" enumerable ")"')
    def element(self, p):
        pass

    @_("STR", "FLOAT", "enumerable")
    def element(self, p):
        pass

    @_("INT", "lvalue")
    def enumerable(self, p):
        pass

    @_("ID", "ID enum_list ")
    def lvalue(self, p):
        pass

    @_('"[" enumerable "," enumerable "]"')
    def enum_list(self, p):
        pass

    @_('ID "\'" ')
    def element(self, p):
        pass

    @_('"[" vector "]"')
    def element(self, p):
        pass

    @_('"(" expr ")"')
    def expr(self, p):
        pass

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        pass

    @_('"{" lines "}"')
    def line(self, p):
        pass

from sly import Parser
from scanner import Scanner

# rekursja prawostronna
# obliczenia robić poziomami (dodawanie liczbowe i dodawanie macierzowe w jednym priorytecie)


class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = "parser.out"

    precedence = (
        ("nonassoc", ":"),
        ("nonassoc", "=", ADD_ASSIGN, SUB_ASSIGN, MUL_ASSIGN, DIV_ASSIGN),
        ("nonassoc", EQ, NEQ, LEQ, GEQ, ">", "<"),
        ("left", "{", "[", "("),
        ("right", "}", "]", ")"),
        ("left", "+", "-", MAT_PLUS, MAT_MINUS),
        ("left", MAT_MUL, MAT_DIV),
        ("left", "*", "/"),
        ("right", UMINUS),
        ("left", IF),
        ("right", ELSE),
        ("left", ","),
    )

    @_("lines line", "line")
    def lines(self, p):
        return ("lines", p[0], p[1]) if len(p) > 1 else p[0]

    @_('PRINT expr ";"', 'RETURN expr ";"')
    def line(self, p):
        return (p[0], p.expr)

    @_('BREAK ";"', 'CONTINUE ";"')
    def line(self, p):
        return (p[0],)

    @_(
        'expressable "=" expr ";"',
        'expressable ADD_ASSIGN expr ";"',
        'expressable SUB_ASSIGN expr ";"',
        'expressable MUL_ASSIGN expr ";"',
        'expressable DIV_ASSIGN expr ";"',
    )
    def line(self, p):
        return ("assign", p.expressable, p.expr)

    @_("IF condition line ELSE line %prec IF", "IF condition line %prec ELSE")
    def line(self, p):
        if len(p) == 6:
            return ("if_else", p.condition, p.line0, p.line1)
        else:
            return ("if", p.condition, p.line)

    @_('"(" statement ")"')
    def condition(self, p):
        return ("condition", p.statement)

    @_(
        "expr EQ expr",
        "expr NEQ expr",
        "expr LEQ expr",
        "expr GEQ expr",
        'expr "<" expr',
        'expr ">" expr',
    )
    def statement(self, p):
        return (p[1], p.expr0, p.expr1)

    @_("ID expr EQ expr", "ID expr NEQ expr")
    def statement(self, p):
        return ("assign_op", p.ID, p.expr0, p.expr1)

    @_('FOR ID "=" enumerable ":" enumerable line', "WHILE condition line")
    def line(self, p):
        if p[0] == "FOR":
            return ("for", p.ID, p.enumerable0, p.enumerable1, p.line)
        else:
            return ("while", p.condition, p.line)

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
        return (p[1], p.expr0, p.expr1)

    @_("vector")
    def expr(self, p):
        return p.vector

    @_("element", 'vector "," element %prec ","')
    def vector(self, p):
        return ("vector", p.element) if len(p) == 1 else ("vector", p[0], p[2])

    @_('ZEROS "(" enumerable ")"', 'EYE "(" enumerable ")"', 'ONES "(" enumerable ")"')
    def element(self, p):
        return (p[0], p.enumerable)

    @_("STR", "FLOAT %prec UMINUS")
    def element(self, p):
        return ("literal", p[0])

    @_("enumerable")
    def element(self, p):
        return p.enumerable

    @_("INT %prec UMINUS")
    def enumerable(self, p):
        return ("int", p.INT)

    @_("expressable")
    def enumerable(self, p):
        return p.expressable

    @_("ID %prec UMINUS", "ID enum_list ")
    def expressable(self, p):
        return ("variable", p.ID) if len(p) == 1 else ("enum_list", p.ID, p.enum_list)

    @_('"[" INT "," INT "]" %prec ","')
    def enum_list(self, p):
        return ("range", p[1], p[3])

    @_('ID "\'" ')
    def element(self, p):
        return ("transpose", p.ID)

    @_('"[" vector "]"')
    def element(self, p):
        return ("vector", p.vector)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ("uminus", p.expr)

    @_('"{" lines "}"')
    def line(self, p):
        return ("block", p.lines)

from sly import Parser
from errors import ParserError
from scanner import Scanner
import AST


def _(*right_side: str) -> any:
    pass


class Mparser(Parser):

    error_list = []
    error_messages = set()
    tokens = Scanner.tokens

    debugfile = "parser.out"

    precedence = (
        ("nonassoc", "EQ", "NEQ", "LEQ", "GEQ", ">", "<"),
        ("left", "+", "-", "MAT_PLUS", "MAT_MINUS"),
        ("left", "*", "/", "MAT_MUL", "MAT_DIV"),
        ("right", "UMINUS"),
        ("left", "IFX"),
        ("right", "ELSE"),
    )

    @_("lines")
    def program(self, p):
        return AST.Program(p[0], p.lineno)

    @_("line lines", "line")
    def lines(self, p):
        if len(p) == 1:
            return AST.Lines(p[0], None, p.lineno)
        else:
            return AST.Lines(p[0], p[1], p.lineno)

    @_('PRINT expr ";"')
    def line(self, p):
        return AST.Print(p[1], p.lineno)

    @_('RETURN expr ";"')
    def line(self, p):
        return AST.Return(p[1], p.lineno)

    @_('BREAK ";"')
    def line(self, p):
        return AST.Break(p.lineno)

    @_('CONTINUE ";"')
    def line(self, p):
        return AST.Continue(p.lineno)

    @_(
        'lvalue "=" expr ";"',
        'lvalue ADD_ASSIGN expr ";"',
        'lvalue SUB_ASSIGN expr ";"',
        'lvalue MUL_ASSIGN expr ";"',
        'lvalue DIV_ASSIGN expr ";"',
    )
    def line(self, p):
        return AST.Assignment(p[0], p[1], p[2], p.lineno)

    @_(
        'IF "(" condition ")" line ELSE line %prec IFX',
        'IF "(" condition ")" line %prec ELSE',
    )
    def line(self, p):
        if len(p) == 7:
            return AST.IfElse(p[2], p[4], p[6], p.lineno)
        else:
            return AST.IfElse(p[2], p[4], None, p.lineno)

    @_(
        "expr EQ expr",
        "expr NEQ expr",
        "expr LEQ expr",
        "expr GEQ expr",
        'expr "<" expr',
        'expr ">" expr',
    )
    def condition(self, p):
        return AST.BinOp(p[1], p[0], p[2], p.lineno)

    @_('FOR ID "=" expr ":" expr line')
    def line(self, p):
        return AST.ForLoop(p[1], p[3], p[5], p[6], p.lineno)

    @_('WHILE "(" condition ")" line')
    def line(self, p):
        return AST.WhileLoop(p[2], p[4], p.lineno)

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
        return AST.BinOp(p[1], p[0], p[2], p.lineno)

    @_("vectors", "matrix", "element")
    def expr(self, p):
        return p[0]

    @_("vector", 'vector "," vectors')
    def vectors(self, p):
        if len(p) == 1:
            return AST.Vector(p[0], p.lineno)
        else:
            return AST.VectorList(p[0], p[2], p.lineno)

    @_('"[" vectors "]"')
    def matrix(self, p):
        return AST.Matrix(p[1], p.lineno)

    @_('ZEROS "(" enumerable ")"', 'EYE "(" enumerable ")"', 'ONES "(" enumerable ")"')
    def element(self, p):
        return AST.MatrixOp(p[0], p[2], None, p.lineno)

    @_(
        'ZEROS "(" enumerable "," enumerable ")"',
        'EYE "(" enumerable "," enumerable ")"',
        'ONES "(" enumerable "," enumerable ")"',
    )
    def element(self, p):
        return AST.MatrixOp(p[0], p[2], p[4], p.lineno)

    @_("enumerable")
    def element(self, p):
        return p[0]

    @_("STR")
    def element(self, p):
        return AST.String(p[0], p.lineno)

    @_("FLOAT")
    def element(self, p):
        return AST.FloatNum(p[0], p.lineno)

    @_("INT")
    def enumerable(self, p):
        return AST.IntNum(p[0], p.lineno)

    @_("lvalue")
    def enumerable(self, p):
        return p[0]

    @_("ID")
    def lvalue(self, p):
        return AST.LValue(p[0], p.lineno)

    @_('ID "[" enumerable "," enumerable "]"')
    def lvalue(self, p):
        return AST.RefValue(p[0], p[2], p[4], p.lineno)

    @_('ID "[" enumerable "]"')
    def lvalue(self, p):
        return AST.RefValue(p[0], p[2], None, p.lineno)

    @_('"[" vector_elements "]"')
    def vector(self, p):
        return p[1]

    @_("element", 'element "," vector_elements')
    def vector_elements(self, p):
        if len(p) == 1:
            return AST.ElementsList(p[0], None, p.lineno)
        else:
            return AST.ElementsList(p[0], p[2], p.lineno)

    @_('ID "\'" ')
    def element(self, p):
        return AST.Transpose(p[0], p.lineno)

    @_('"(" expr ")"')
    def expr(self, p):
        return p[1]

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return AST.UnaryOp(p[0], p[1], p.lineno)

    @_('"{" lines "}"')
    def line(self, p):
        return AST.Block(p[1])

    def error(self, token):
        if token:
            text = f"Syntax error at token '{token.type}' (value: '{token.value}')"
            if text not in self.error_messages:
                self.error_list.append(
                    ParserError(
                        text=text,
                        line_number=token.lineno,
                    )
                )
                self.error_messages.add(text)
        self.errok()

from sly import Parser
from scanner import Scanner
import AST

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

    @_('RETURN expr ";"')
    def line(self, p):
        # return (p[0], p.expr)
        return AST.Return(p)
    
    @_('PRINT expr ";"')
    def line(self, p):
        # return (p[0], p.expr)
        return AST.Print(p)

    @_('BREAK ";"')
    def line(self, p):
        # return (p[0],)
        return AST.Break(p)
    
    @_('CONTINUE ";"')
    def line(self, p):
        # return (p[0],)
        return AST.Continue(p)

    @_(
        'expressable "=" expr ";"',
        'expressable ADD_ASSIGN expr ";"',
        'expressable SUB_ASSIGN expr ";"',
        'expressable MUL_ASSIGN expr ";"',
        'expressable DIV_ASSIGN expr ";"',
    )
    def line(self, p):
        # return ("assign", p.expressable, p.expr)
        return AST.Assignment(p)

    @_("IF condition line ELSE line %prec IF", "IF condition line %prec ELSE")
    def line(self, p):
        # if len(p) == 6:
            # return ("if_else", p.condition, p.line0, p.line1)
        # else:
            # return ("if", p.condition, p.line)
        return AST.IfElse(p)

    @_('"(" statement ")"')
    def condition(self, p):
        # return ("condition", p.statement)
        return AST.Condition(p)

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

    @_('FOR ID "=" enumerable ":" enumerable line')
    def line(self, p):
        # return ("for", p.ID, p.enumerable0, p.enumerable1, p.line)
        return AST.ForLoop(p)
    
    @_("WHILE condition line")
    def line(self, p):
        # return ("while", p.condition, p.line)
        return AST.WhileLoop(p)

    @_(
        'expr "+" expr',
        'expr "-" expr',
        'expr "*" expr',
        'expr "/" expr',
    )
    def expr(self, p):
        # return (p[1], p.expr0, p.expr1)
        return AST.BinOp(p)
    
    @_(
        "expr MAT_PLUS expr",
        "expr MAT_MINUS expr",
        "expr MAT_MUL expr",
        "expr MAT_DIV expr",
    )
    def expr(self, p):
        # return (p[1], p.expr0, p.expr1)
        return AST.MatrixOp(p)

    @_("vector")
    def expr(self, p):
        return p.vector

    @_("element", 'vector "," element %prec ","')
    def vector(self, p):
        return ("vector", p.element) if len(p) == 1 else ("vector", p[0], p[2])

    @_('ZEROS "(" enumerable ")"', 'EYE "(" enumerable ")"', 'ONES "(" enumerable ")"')
    def element(self, p):
        return (p[0], p.enumerable)

    @_("FLOAT %prec UMINUS")
    def element(self, p):
        # return ("literal", p[0])
        return AST.FloatLiteral(p)
    
    @_("STR")
    def element(self, p):
        # return ("literal", p[0])
        return AST.StringLiteral(p)

    @_("enumerable")
    def element(self, p):
        return p.enumerable

    @_("INT %prec UMINUS")
    def enumerable(self, p):
        # return ("int", p.INT)
        return AST.IntLiteral(p)

    @_("expressable")
    def enumerable(self, p):
        return p.expressable

    @_("ID %prec UMINUS", "ID enum_list ")
    def expressable(self, p):
        #return ("variable", p.ID) if len(p) == 1 else ("enum_list", p.ID, p.enum_list)
        return AST.Variable(p)

    @_('"[" INT "," INT "]" %prec ","')
    def enum_list(self, p):
        return ("range", p[1], p[3])

    @_('ID "\'" ')
    def element(self, p):
        # return ("transpose", p.ID)
        return AST.Transpose(p)

    @_('"[" vector "]"')
    def element(self, p):
        # return ("vector", p.vector)
        return AST.Vector(p)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        # return ("uminus", p.expr)
        return AST.UnaryOp(p)

    @_('"{" lines "}"')
    def line(self, p):
        # return ("block", p.lines)
        return AST.Block(p)

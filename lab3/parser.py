from sly import Parser
from scanner import Scanner

# rekursja prawostronna
# obliczenia robić poziomami (dodawanie liczbowe i dodawanie macierzowe w jednym priorytecie)

class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'

    precedence = (
        ('nonassoc', ":"),
        ('nonassoc', "=", ADD_ASSIGN, SUB_ASSIGN, MUL_ASSIGN, DIV_ASSIGN),
        ('nonassoc', EQ, NEQ, LEQ, GEQ, ">", "<"),
        ("left", "{", "[", "("),
        ("right", "}", "]", ")"),
        ('left', "+", "-", MAT_PLUS, MAT_MINUS),
        ('left',  MAT_MUL, MAT_DIV),
        ('left', "*", "/"), 
        ('right', UMINUS), 
        ('left', IF),
        ("right", ELSE),
        ("left", ","),
    )

    @_('lines line',
       'line')
    def lines(self, p):
        pass

    @_('PRINT expr ";"',
       'RETURN expr ";"')
    def line(self, p):
        pass

    @_('BREAK ";"',
       'CONTINUE ";"')
    def line(self, p):
        pass
    
    @_('expressable "=" expr ";"',
       'expressable ADD_ASSIGN expr ";"',
       'expressable SUB_ASSIGN expr ";"',
       'expressable MUL_ASSIGN expr ";"',
       'expressable DIV_ASSIGN expr ";"')
    def line(self, p):
        pass

    @_('IF condition line ELSE line %prec IF',
       'IF condition line %prec ELSE')
    def line(self, p):
        pass

    @_('"(" statement ")"')
    def condition(self, p):
        pass

    @_('expr EQ expr',
       'expr NEQ expr',
       'expr LEQ expr',
       'expr GEQ expr',
       'expr "<" expr',
       'expr ">" expr')
    def statement(self, p):
        pass

    @_('ID expr EQ expr',
       'ID expr NEQ expr')
    def statement(self, p):
        pass

    @_('FOR ID "=" enumerable ":" enumerable line',
       'WHILE condition line')
    def line(self, p):
        pass
    
    @_('expr "+" expr',
       'expr "-" expr',
       'expr MAT_PLUS expr',
       'expr MAT_MINUS expr',
       'expr "*" expr',
       'expr "/" expr',
       'expr MAT_MUL expr',
       'expr MAT_DIV expr')
    def expr(self, p):
        pass

    @_('vector')
    def expr(self, p):
        pass
    
    @_('element',
       'vector "," element %prec ","')
    def vector(self, p):
        pass

    @_('ZEROS "(" enumerable ")"', 
       'EYE "(" enumerable ")"',
       'ONES "(" enumerable ")"')
    def element(self, p):
        pass

    @_('STR', 'FLOAT %prec UMINUS')
    def element(self, p):
        pass

    @_('enumerable')
    def element(self, p):
        pass

    @_('INT %prec UMINUS')
    def enumerable(self, p):
        pass

    @_('expressable')
    def enumerable(self, p):
        pass

    @_('ID %prec UMINUS',
       'ID enum_list ')
    def expressable(self, p):
        pass

    @_('"[" INT "," INT "]" %prec ","')
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

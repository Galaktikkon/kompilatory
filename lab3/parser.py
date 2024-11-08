from sly import Parser
from scanner import Scanner

# rekursja prawostronna
# obliczenia robić poziomami (dodawanie liczbowe i dodawanie macierzowe w jednym priorytecie)

class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'


    precedence = (
        ('nonassoc', ":"),
        ('left', "+", "-", MAT_PLUS, MAT_MINUS),
        ('left',  MAT_MUL, MAT_DIV),
        ('left', "*", "/"), 
        ("left", ","),
        ('right', UMINUS), 
        ("right", ELSE),
    )

    @_('lines')
    def body(self, p):
        pass

    @_('lines line')
    def lines(self, p):
        pass
    
    @_('line')
    def lines(self, p):
        pass

    @_('PRINT expr ";"')
    def line(self, p):
        pass
    
    @_('assignment ";"')
    def line(self, p):
        pass
    
    @_('ID "=" expr',
       'ID ADD_ASSIGN expr',
       'ID SUB_ASSIGN expr',
       'ID MUL_ASSIGN expr',
       'ID DIV_ASSIGN expr')
    def assignment(self, p):
        pass

    @_('ID expr "=" expr')
    def assignment(self, p):
        pass

    @_('control_statement ";"')
    def line(self, p):
        pass

    @_('BREAK',
       'CONTINUE')
    def control_statement(self, p):
        pass

    @_('return_statement ";"')
    def line(self, p):
        pass

    @_('RETURN expr')
    def return_statement(self, p):
        pass

    @_('"{" body "}"')
    def line(self, p):
        pass

    @_('if_statement')
    def line(self, p):
        pass

    @_('IF condition line ELSE line ',
       'IF condition line %prec ELSE')
    def if_statement(self, p):
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

    @_('loop')
    def line(self, p):
        pass

    @_('FOR ID "=" enumerable ":" enumerable line',
       'WHILE condition line')
    def loop(self, p):
        pass
    
    @_('expr "+" expr',
       'expr "-" expr',
       'expr MAT_PLUS expr',
       'expr MAT_MINUS expr')
    def expr(self, p):
        pass
    
    @_('expr "*" expr',
       'expr "/" expr',
       'expr MAT_MUL expr',
       'expr MAT_DIV expr')
    def expr(self, p):
        pass
    
    @_('expr "," element')
    def expr(self, p):
        pass

    @_('element')
    def expr(self, p):
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

    @_('INT %prec UMINUS', 'ID %prec UMINUS')
    def enumerable(self, p):
        pass

    @_('ID "\'" ')
    def element(self, p):
        pass

    @_('"[" expr "]"')
    def element(self, p):
        pass

    @_('"(" expr ")"')
    def element(self, p):
        pass

    @_('"-" expr %prec UMINUS')
    def element(self, p):
        pass

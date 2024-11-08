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

    @_('print_statement ";"')
    def line(self, p):
        pass

    @_('PRINT expr')
    def print_statement(self, p):
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

    @_('ID "[" factor "]" "=" expr')
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

    @_('IF condition "{" body "}" ELSE "{" body "}" ',
       'IF condition "{" body "}" %prec ELSE')
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

    @_('ID factor EQ expr',
       'ID factor NEQ expr')
    def statement(self, p):
        pass

    @_('loop')
    def line(self, p):
        pass

    @_('FOR ID "=" enumerable ":" enumerable "{" body "}"',
       'WHILE condition "{" body "}"')
    def loop(self, p):
        pass
    
    @_('expr "+" term',
       'expr "-" term',
       'expr MAT_PLUS term',
       'expr MAT_MINUS term')
    def expr(self, p):
        pass

    @_('term %prec')
    def expr(self, p):
        # return p.term
        pass
        
    @_('term "*" factor',
       'term "/" factor',
       'term MAT_MUL factor',
       'term MAT_DIV factor')
    def term(self, p):
        pass

    @_('factor %prec ","')
    def term(self, p):
        # return p.factor
        pass
    
    @_('factor "," element')
    def factor(self, p):
        pass

    @_('element')
    def factor(self, p):
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

    @_('"[" factor "]"')
    def element(self, p):
        pass

    @_('"(" expr ")"')
    def element(self, p):
        pass

    @_('"-" expr %prec UMINUS')
    def element(self, p):
        pass

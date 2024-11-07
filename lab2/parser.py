from sly import Parser
from scanner import Scanner

# rekursja prawostronna
# obliczenia robić poziomami (dodawanie liczbowe i dodawanie macierzowe w jednym priorytecie)

class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'


    precedence = (
        ('nonassoc', "=", ADD_ASSIGN, SUB_ASSIGN, MUL_ASSIGN, DIV_ASSIGN, LEQ, GEQ, EQ, NEQ),
        ('left', "+", "-", MAT_PLUS, MAT_MINUS),
        ('left', "*", "/", MAT_MUL, MAT_DIV)
    )


    @_('body line')
    def body(p):
        pass
    
    @_('line')
    def body(p):
        pass

    @_('PRINT expr ";"')
    def line(p):
        pass

    @_('ID "=" expr ";"',
       'ID ADD_ASSIGN expr ";"',
       'ID SUB_ASSIGN expr ";"',
       'ID MUL_ASSIGN expr ";"',
       'ID DIV_ASSIGN expr ";"')
    def line(p):
        pass

    @_('BREAK ";"',
       'CONTINUE ";"')
    def line(p):
        pass

    @_('RETURN expr')
    def line(p):
        pass

    @_('"{" body "}"')
    def line(p):
        pass

    @_('IF condition body',
       'WHILE condition body')
    def line(p):
        pass

    @_('ELSE body')
    def line(p):
        pass

    @_('"(" expr EQ expr ")"',
       '"(" expr NEQ expr ")"',
       '"(" expr LEQ expr ")"',
       '"(" expr GEQ expr ")"')
    def condition(p):
        pass

    @_('FOR ID "=" INT ":" INT body')
    def line(p):
        pass
    
    @_('expr "+" term',
       'expr "-" term',
       'expr MAT_PLUS term',
       'expr MAT_MINUS term')
    def expr(p):
        pass

    @_('term')
    def expr(p):
        # return p.term
        pass

    @_('term "*" factor',
       'term "/" factor',
       'term MAT_MUL factor',
       'term MAT_DIV factor')
    def term(p):
        pass

    @_('factor')
    def term(p):
        # return p.factor
        pass
    
    @_('factor "," element')
    def factor(p):
        pass

    @_('element')
    def factor(p):
        pass

    @_('ZEROS "(" INT ")"', 
       'EYE "(" INT ")"',
       'ONES "(" INT ")"')
    def element(p):
        pass

    @_('FLOAT',
       'INT',
       'STR')
    def element(p):
        pass

    @_('"[" element "]"')
    def element(p):
        pass


    @_('"[" factor "]"')
    def element(p):
        pass

    
    @_('"(" expr ")"')
    def element(p):
        pass
    
from sly import Parser
from scanner import Scanner

# rekursja prawostronna
# obliczenia robić poziomami (dodawanie liczbowe i dodawanie macierzowe w jednym priorytecie)

class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'


    precedence = (
    )


    @_('body line')
    def body(self, p):
        pass
    
    @_('line')
    def body(self, p):
        pass

    @_('PRINT expr ";"')
    def line(self, p):
        pass

    @_('ID "=" expr ";"',
       'ID ADD_ASSIGN expr ";"',
       'ID SUB_ASSIGN expr ";"',
       'ID MUL_ASSIGN expr ";"',
       'ID DIV_ASSIGN expr ";"')
    def line(self, p):
        pass

    @_('BREAK ";"',
       'CONTINUE ";"')
    def line(self, p):
        pass

    @_('RETURN expr ";"')
    def line(self, p):
        pass

    @_('"{" body "}"')
    def line(self, p):
        pass

    @_('IF condition body',
       'WHILE condition body')
    def line(self, p):
        pass

    @_('ELSE body')
    def line(self, p):
        pass

    @_('"(" expr EQ expr ")"',
       '"(" expr NEQ expr ")"',
       '"(" expr LEQ expr ")"',
       '"(" expr GEQ expr ")"',
       '"(" expr "<" expr ")"',
       '"(" expr ">" expr ")"')
    def condition(self, p):
        pass

    @_('FOR ID "=" element ":" element body')
    def line(self, p):
        pass
    
    @_('expr "+" term',
       'expr "-" term',
       'expr MAT_PLUS term',
       'expr MAT_MINUS term')
    def expr(self, p):
        pass

    @_('term')
    def expr(self, p):
        # return p.term
        pass

    @_('term "*" factor',
       'term "/" factor',
       'term MAT_MUL factor',
       'term MAT_DIV factor')
    def term(self, p):
        pass

    @_('factor')
    def term(self, p):
        # return p.factor
        pass
    
    @_('factor "," element')
    def factor(self, p):
        pass

    @_('element')
    def factor(self, p):
        pass

    @_('ZEROS "(" INT ")"', 
       'EYE "(" INT ")"',
       'ONES "(" INT ")"')
    def element(self, p):
        pass

    @_('FLOAT',
       'INT',
       'STR',
       'ID')
    def element(self, p):
        pass

    @_('"[" element "]"')
    def element(self, p):
        pass

    @_('"[" factor "]"')
    def element(self, p):
        pass

    @_('"(" expr ")"')
    def element(self, p):
        pass
    
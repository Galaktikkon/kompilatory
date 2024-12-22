class Node(object):
    def print_tree(self, level=0):
        raise NotImplementedError("printTree not implemented for this class")
    def accept(self, visitor):
        return visitor.visit(self)


class Program(Node):
    def __init__(self, lines, line_number=None):
        self.lines = lines
        self.line_number = line_number


class Lines(Node):
    def __init__(self, line, lines=None, line_number=None):
        self.lines = lines
        self.line = line
        self.line_number = line_number


class Print(Node):
    def __init__(self, expr, line_number=None):
        self.expr = expr
        self.line_number = line_number


class Return(Node):
    def __init__(self, expr, line_number=None):
        self.expr = expr
        self.line_number = line_number


class Break(Node):
    def __init__(self, line_number=None):
        super().__init__()
        self.line_number = line_number


class Continue(Node):
    def __init__(self, line_number=None):
        super().__init__()
        self.line_number = line_number


class Assignment(Node):
    def __init__(self, variable, op, expr, line_number=None):
        self.variable = variable
        self.expr = expr
        self.op = op
        self.line_number = line_number


class IfElse(Node):
    def __init__(self, condition, if_branch, else_branch=None, line_number=None):
        self.condition = condition
        self.if_branch = if_branch
        self.else_branch = else_branch
        self.line_number = line_number


class BinOp(Node):
    def __init__(self, op, left, right, line_number=None):
        self.op = op
        self.left = left
        self.right = right
        self.line_number = line_number


class ForLoop(Node):
    def __init__(self, variable, start, end, body, line_number=None):
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body
        self.line_number = line_number


class WhileLoop(Node):
    def __init__(self, condition, body, line_number=None):
        self.condition = condition
        self.body = body
        self.line_number = line_number


class Vector(Node):
    def __init__(self, vector_elements, line_number=None):
        self.vector_elements = vector_elements
        self.line_number = line_number


class VectorList(Node):
    def __init__(self, vector, vectors=None, line_number=None):
        self.vector = vector
        self.vectors = vectors
        self.line_number = line_number


class Matrix(Node):
    def __init__(self, vectors, line_number=None):
        self.vectors = vectors
        self.line_number = line_number


class MatrixOp(Node):
    def __init__(self, type, enumerable1, enumerable2=None, line_number=None):
        self.type = type
        self.enumerable1 = enumerable1
        self.enumerable2 = enumerable2
        self.line_number = line_number


class String(Node):
    def __init__(self, value, line_number=None):
        self.value = value
        self.line_number = line_number


class FloatNum(Node):
    def __init__(self, value, line_number=None):
        self.value = value
        self.line_number = line_number


class IntNum(Node):
    def __init__(self, value, line_number=None):
        self.value = value
        self.line_number = line_number


class LValue(Node):
    def __init__(self, identifier, line_number=None):
        self.identifier = identifier
        self.line_number = line_number


class RefValue(Node):
    def __init__(self, identifier, row, col=None, line_number=None):
        self.identifier = identifier
        self.row = row
        self.col = col
        self.line_number = line_number


class ElementsList(Node):
    def __init__(self, element, element_list=None, line_number=None):
        self.element = element
        self.element_list = element_list
        self.line_number = line_number


class Transpose(Node):
    def __init__(self, identifier, line_number=None):
        self.identifier = identifier
        self.line_number = line_number


class UnaryOp(Node):
    def __init__(self, op, operand, line_number=None):
        self.operator = op
        self.operand = operand
        self.line_number = line_number


class Block(Node):
    def __init__(self, lines):
        self.lines = lines

class Node(object):
    def print_tree(self, level=0):
        raise NotImplementedError("printTree not implemented for this class")


class Lines(Node):
    def __init__(self, line, lines=None):
        self.lines = lines
        self.line = line


class Print(Node):
    def __init__(self, expr):
        self.expr = expr


class Return(Node):
    def __init__(self, expr):
        self.expr = expr


class Break(Node):
    def __init__(self):
        super().__init__()


class Continue(Node):
    def __init__(self):
        super().__init__()


class Assignment(Node):
    def __init__(self, variable, op, expr):
        self.variable = variable
        self.expr = expr
        self.op = op


class IfElse(Node):
    def __init__(self, condition, if_branch, else_branch=None):
        self.condition = condition
        self.if_branch = if_branch
        self.else_branch = else_branch


class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class ForLoop(Node):
    def __init__(self, variable, start, end, body):
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body


class WhileLoop(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class Vector(Node):
    def __init__(self, vector):
        self.vector = vector


class VectorList(Node):
    def __init__(self, vector, vectors=None):
        self.vector = vector
        self.vectors = vectors


class Matrix(Node):
    def __init__(self, vectors):
        self.vectors = vectors


class MatrixOp(Node):
    def __init__(self, type, enumerable):
        self.type = type
        self.enumerable = enumerable


class String(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class LValue(Node):
    def __init__(self, identifier, enum_list=None):
        self.identifier = identifier
        self.enum_list = enum_list


class RefValue(Node):
    def __init__(self, identifier, ref):
        self.identifier = identifier
        self.ref = ref


class ElementsList(Node):
    def __init__(self, enumerable, enum_list=None):
        self.enumerable = enumerable
        self.enum_list = enum_list


class EnumerableList(Node):
    def __init__(self, enumerable, enum_list=None):
        self.enumerable = enumerable
        self.enum_list = enum_list


class Transpose(Node):
    def __init__(self, identifier):
        self.identifier = identifier


class UnaryOp(Node):
    def __init__(self, op, operand):
        self.operator = op
        self.operand = operand

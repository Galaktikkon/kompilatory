class Node(object):
    def printTree(self, level=0):
        raise NotImplementedError("printTree not implemented for this class")


class Lines(Node):
    def __init__(self, lines, line=None):
        self.lines = lines
        self.line = line


class Line(Node):
    def __init__(self, line):
        self.line = line


class BinOp(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right


class UnaryOp(Node):
    def __init__(self, op, operand):
        self.operator = op
        self.operand = operand


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


class Block(Node):
    def __init__(self, statements):
        self.statements = statements

    def printTree(self, indent=""):
        print(f"{indent}{{")
        for stmt in self.statements:
            stmt.printTree(indent + "  ")
        print(f"{indent}}}")


class Break(Node):
    def __init__(self):
        super().__init__()


class Continue(Node):
    def __init__(self):
        super().__init__()


class Return(Node):
    def __init__(self, expr):
        self.expr = expr


class Print(Node):
    def __init__(self, expr):
        self.expr = expr


class Vector(Node):
    def __init__(self, elements):
        self.elements = elements


class Transpose(Node):
    def __init__(self, variable):
        self.variable = variable

    def printTree(self, indent=""):
        print(f"{indent}TRANSPOSE")
        self.variable.printTree(indent + "  ")


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Identifier(Node):
    def __init__(self, value):
        self.value = value

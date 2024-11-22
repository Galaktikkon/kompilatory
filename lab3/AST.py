class Node(object):
    def printTree(self, level=0):
        raise NotImplementedError("printTree not implemented for this class")


class IntLiteral(Node):
    def __init__(self, value):
        self.value = value

    def printTree(self, indent=""):
        print(f"{indent}{self.value}")


class FloatLiteral(Node):
    def __init__(self, value):
        self.value = value

    def printTree(self, indent=""):
        print(f"{indent}{self.value}")


class StringLiteral(Node):
    def __init__(self, value):
        self.value = value

    def printTree(self, indent=""):
        print(f'{indent}"{self.value}"')


class Variable(Node):
    def __init__(self, name):
        self.name = name

    def printTree(self, indent=""):
        print(f"{indent}{self.name}")


class BinOp(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def printTree(self, indent=""):
        print(f"{indent}{self.operator}")
        self.left.printTree(indent + "  ")
        self.right.printTree(indent + "  ")


class UnaryOp(Node):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def printTree(self, indent=""):
        print(f"{indent}{self.operator}")
        self.operand.printTree(indent + "  ")


class Assignment(Node):
    def __init__(self, variable, expr):
        self.variable = variable
        self.expr = expr

    def printTree(self, indent=""):
        print(f"{indent}=")
        self.variable.printTree(indent + "  ")
        self.expr.printTree(indent + "  ")


class IfElse(Node):
    def __init__(self, condition, if_branch, else_branch=None):
        self.condition = condition
        self.if_branch = if_branch
        self.else_branch = else_branch

    def printTree(self, indent=""):
        print(f"{indent}IF")
        self.condition.printTree(indent + "  ")
        self.if_branch.printTree(indent + "  ")
        if self.else_branch:
            print(f"{indent}ELSE")
            self.else_branch.printTree(indent + "  ")


class ForLoop(Node):
    def __init__(self, variable, start, end, body):
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body

    def printTree(self, indent=""):
        print(f"{indent}FOR {self.variable.name}")
        print(f"{indent}  FROM")
        self.start.printTree(indent + "    ")
        print(f"{indent}  TO")
        self.end.printTree(indent + "    ")
        print(f"{indent}  DO")
        self.body.printTree(indent + "    ")


class WhileLoop(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def printTree(self, indent=""):
        print(f"{indent}WHILE")
        self.condition.printTree(indent + "  ")
        print(f"{indent}DO")
        self.body.printTree(indent + "  ")


class Block(Node):
    def __init__(self, statements):
        self.statements = statements

    def printTree(self, indent=""):
        print(f"{indent}{{")
        for stmt in self.statements:
            stmt.printTree(indent + "  ")
        print(f"{indent}}}")


class Break(Node):
    def printTree(self, indent=""):
        print(f"{indent}BREAK")


class Continue(Node):
    def printTree(self, indent=""):
        print(f"{indent}CONTINUE")


class Return(Node):
    def __init__(self, expr):
        self.expr = expr

    def printTree(self, indent=""):
        print(f"{indent}RETURN")
        self.expr.printTree(indent + "  ")


class Print(Node):
    def __init__(self, expr):
        self.expr = expr

    def printTree(self, indent=""):
        print(f"{indent}PRINT")
        self.expr.printTree(indent + "  ")


class MatrixOp(Node):
    def __init__(self, operation, size):
        self.operation = operation
        self.size = size

    def printTree(self, indent=""):
        print(f"{indent}{self.operation}")
        self.size.printTree(indent + "  ")


class Vector(Node):
    def __init__(self, elements):
        self.elements = elements

    def printTree(self, indent=""):
        print(f"{indent}VECTOR")
        for elem in self.elements:
            elem.printTree(indent + "  ")


class Transpose(Node):
    def __init__(self, variable):
        self.variable = variable

    def printTree(self, indent=""):
        print(f"{indent}TRANSPOSE")
        self.variable.printTree(indent + "  ")


class Condition(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def printTree(self, indent=""):
        print(f"{indent}{self.operator}")
        self.left.printTree(indent + "  ")
        self.right.printTree(indent + "  ")

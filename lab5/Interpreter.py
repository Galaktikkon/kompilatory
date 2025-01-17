import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys
import numpy as np

sys.setrecursionlimit(10000)

operations = {
    "+": (lambda x, y: x + y),
    "+=": (lambda x, y: x + y),
    "-": (lambda x, y: x - y),
    "-=": (lambda x, y: x - y),
    "*": (lambda x, y: x * y),
    "*=": (lambda x, y: x * y),
    "/": (lambda x, y: x / y),
    "/=": (lambda x, y: x / y),
    "==": (lambda x, y: x == y),
    "!=": (lambda x, y: x != y),
    ">=": (lambda x, y: x >= y),
    ">": (lambda x, y: x > y),
    "<=": (lambda x, y: x <= y),
    "<": (lambda x, y: x < y),
    ".+": (lambda x, y: (np.matrix(x) + np.matrix(y))),
    ".-": (lambda x, y: (np.matrix(x) - np.matrix(y))),
    ".*": (lambda x, y: np.multiply(np.array(x), np.array(y))),
    "./": (lambda x, y: np.divide(np.array(x), np.array(y))),
}


class Interpreter(object):
    def __init__(self):
        self.mem_stack = MemoryStack()

    @on("node")
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        node.lines.accept(self)

    @when(AST.Lines)
    def visit(self, node):
        node.line.accept(self)
        if node.lines != None:
            node.lines.accept(self)

    @when(AST.Print)
    def visit(self, node):
        expr1 = node.expr1.accept(self)
        if node.expr2 != None:
            expr2 = node.expr2.accept(self)
            print(f"{expr1}, {expr2}")
        else:
            print(expr1)

    @when(AST.Return)
    def visit(self, node):
        return node.expr.accept(self)

    @when(AST.Break)
    def visit(self, node):
        raise BreakException

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException

    @when(AST.Assignment)
    def visit(self, node):
        expr = node.expr.accept(self)
        op = node.op
        if op == "=":
            if isinstance(node.variable, AST.RefValue):
                tmp = np.array(self.mem_stack.get(node.variable.identifier))
                row, col = node.variable.row.accept(self), node.variable.col.accept(
                    self
                )
                if col != None:
                    tmp[row][col] = expr
                else:
                    tmp[row] = expr
                self.mem_stack.set(node.variable.identifier, tmp)
            else:
                self.mem_stack.set(node.variable.identifier, expr)
        else:
            left = self.mem_stack.get(node.variable.identifier)
            result = operations[op](left, expr)
            self.mem_stack.set(node.variable.identifier, result)

    @when(AST.IfElse)
    def visit(self, node):
        if node.condition.accept(self):
            self.mem_stack.push(Memory("if"))
            try:
                result = node.if_branch.accept(self)
            finally:
                self.mem_stack.pop()
            return result
        elif not node.condition.accept(self) and node.else_branch is not None:
            self.mem_stack.push(Memory("else"))
            try:
                result = node.else_branch.accept(self)
            finally:
                self.mem_stack.pop()
            return result

    @when(AST.BinOp)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        op = node.op
        return operations[op](left, right)

    @when(AST.ForLoop)
    def visit(self, node):
        start = node.start.accept(self)
        end = node.end.accept(self)
        self.mem_stack.push(Memory("for"))
        self.mem_stack.set(node.id, start)
        iterator = self.mem_stack.get(node.id)
        while iterator < end:
            try:
                node.body.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
            self.mem_stack.set(node.id, iterator + 1)
            iterator = self.mem_stack.get(node.id)
        self.mem_stack.pop()

    @when(AST.WhileLoop)
    def visit(self, node):
        self.mem_stack.push(Memory("while"))
        while node.condition.accept(self):
            try:
                node.body.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        self.mem_stack.pop()

    @when(AST.Vector)
    def visit(self, node):
        node.vector_elements.accept(self)

    @when(AST.VectorList)
    def visit(self, node):
        node.vector.accept(self)
        if node.vectors != None:
            node.vectors.accept(self)

    @when(AST.Matrix)
    def visit(self, node):
        node.vectors.accept(self)

    @when(AST.MatrixOp)
    def visit(self, node):
        type = node.type
        x = node.enumerable1.accept(self)
        if node.enumerable2 == None:
            y = 1
        else:
            y = node.enumerable2.accept(self)
        if type == "zeros":
            return np.zeros((x, y)).tolist()
        elif type == "ones":
            return np.ones((x, y)).tolist()
        elif type == "eye":
            if node.enumerable2 == None:
                y = None
            return np.eye(x, y).tolist()

    @when(AST.String)
    def visit(self, node):
        return str(node.value[1:-1])

    @when(AST.FloatNum)
    def visit(self, node):
        return float(node.value)

    @when(AST.IntNum)
    def visit(self, node):
        return int(node.value)

    @when(AST.LValue)
    def visit(self, node):
        return self.mem_stack.get(node.identifier)

    @when(AST.RefValue)
    def visit(self, node):
        row = node.row.accept(self)
        column = node.col.accept(self)
        return self.mem_stack.get(node.identifier)[row][column]

    @when(AST.ElementsList)
    def visit(self, node):
        node.element.accept(self)
        if node.element_list != None:
            node.element_list.accept(self)

    @when(AST.Transpose)
    def visit(self, node):
        array = self.mem_stack.get(node.identifier)
        return array.T

    @when(AST.UnaryOp)
    def visit(self, node):
        operand = node.operand.accept(self)
        if node.operator == "-":
            operand = -1 * operand
        return operand

    @when(AST.Block)
    def visit(self, node):
        node.lines.accept(self)


import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
import numpy as np

sys.setrecursionlimit(10000)

operations = {
    '+': (lambda x, y: x + y),
    '+=': (lambda x, y: x + y),
    '-': (lambda x, y: x - y),
    '-=': (lambda x, y: x - y),
    '*': (lambda x, y: x * y),
    '*=': (lambda x, y: x * y),
    '/': (lambda x, y: x / y),
    '/=': (lambda x, y: x / y),

    '==': (lambda x, y: x == y),
    '!=': (lambda x, y: x != y),
    '>=': (lambda x, y: x >= y),
    '>': (lambda x, y: x > y),
    '<=': (lambda x, y: x <= y),
    '<': (lambda x, y: x < y),

    '.+': (lambda x, y: (np.matrix(x) + np.matrix(y)).tolist()),
    '.-': (lambda x, y: (np.matrix(x) - np.matrix(y)).tolist()),
    '.*': (lambda x, y: np.multiply(np.array(x), np.array(y)).tolist()),
    './': (lambda x, y: np.divide(np.array(x), np.array(y)).tolist())
}

class Interpreter(object):
    def __init__(self):
        self.mem_stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        node.lines.accept(self)

    @when(AST.Lines)
    def visit(self, node):
        if node.lines is not None:
            node.lines.accept(self)
        node.line.accept(self)

    @when(AST.Print)
    def visit(self, node):
        print(" ".join([str(element.accept(self)) for element in [node.expr]]))

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
        variable = node.variable.accept(self)
        expr = node.expr.accept(self)
        op = node.op
        if op == '=':
            if isinstance(variable, AST.RefValue):
                tmp = np.array(self.mem_stack.get(variable.name))
                indexes = tuple([i.accept(self) for i in variable.indexes.indexes])
                tmp[indexes] = expr
                self.mem_stack.set(variable.name, tmp.tolist())
            else:
                self.mem_stack.set(variable.name, expr)
        else:
            left = self.mem_stack.get(variable.name)
            result = operations[op](left, expr)
            self.mem_stack.set(variable.name, result)

    @when(AST.IfElse)
    def visit(self, node):
        if node.condition.accept(self):
            self.mem_stack.push(Memory("if"))
            result = node.if_branch.accept(self)
            self.mem_stack.pop()
            return result
        elif not node.condition.accept(self) and node.else_branch is not None:
            self.mem_stack.push(Memory("else"))
            result = node.else_branch.accept(self)
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
        print(node.variable)
        variable = node.variable.accept(self)
        start = node.start.accept(self)
        end = node.end.accept(self)

        self.mem_stack.set(variable.name, start)
        while variable < end:
            try:
                node.body.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        variable = node.variable.accept(self) + 1
        self.mem_stack.set(variable.name, variable)

    @when(AST.WhileLoop)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.body.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue

    @when(AST.Vector)
    def visit(self, node):
        return [n.accept(self) for n in node.vector_elements]

    # TODO
    @when(AST.VectorList)
    def visit(self, node):
        pass


    @when(AST.Matrix)
    def visit(self, node):
        return [n.accept(self) for n in node.vectors]

    @when(AST.MatrixOp)
    def visit(self, node):
        type = node.type
        enumerable = node.enumerable.accept(self)
        if type == 'zeros':
            return np.zeros(enumerable).tolist()
        elif type == 'ones':
            return np.ones(enumerable).tolist()
        elif type == 'eye':
            return np.eye(enumerable).tolist()

    @when(AST.String)
    def visit(self, node):
        return node.value[1:-1]

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value
    
    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.LValue)
    def visit(self, node):
        return self.mem_stack.get(node.identifier)

    @when(AST.RefValue)
    def visit(self, node):
        row = node.row.accept(self)
        column = node.column.accept(self)
        return self.mem_stack.get(node.identifier)[row][column]

    # TODO
    @when(AST.ElementsList)
    def visit(self, node):
        pass

    @when(AST.Transpose)
    def visit(self, node):
        array = self.mem_stack.get(node.identifier)
        return array.T
        
    @when(AST.UnaryOp)
    def visit(self, node):
        operand = node.operand.accept(self)
        if node.operatoe == "-":
            operand = -1 * operand
        return operand

    # TODO
    @when(AST.Block)
    def visit(self, node):
        pass


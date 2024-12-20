#!/usr/bin/python

import AST
from collections import defaultdict
from SymbolTable import SymbolTable


ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

ttype["+"]["int"]["int"] = "int"
ttype["-"]["int"]["int"] = "int"
ttype["*"]["int"]["int"] = "int"
ttype["/"]["int"]["int"] = "int"
ttype["<"]["int"]["int"] = "logic"
ttype[">"]["int"]["int"] = "logic"
ttype["<="]["int"]["int"] = "logic"
ttype[">="]["int"]["int"] = "logic"
ttype["=="]["int"]["int"] = "logic"
ttype["!="]["int"]["int"] = "logic"

ttype["+"]["int"]["float"] = "float"
ttype["-"]["int"]["float"] = "float"
ttype["*"]["int"]["float"] = "float"
ttype["/"]["int"]["float"] = "float"
ttype["<"]["int"]["float"] = "logic"
ttype[">"]["int"]["float"] = "logic"
ttype["<="]["int"]["float"] = "logic"
ttype[">="]["int"]["float"] = "logic"
ttype["=="]["int"]["float"] = "logic"
ttype["!="]["int"]["float"] = "logic"

ttype["+"]["float"]["int"] = "float"
ttype["-"]["float"]["int"] = "float"
ttype["*"]["float"]["int"] = "float"
ttype["/"]["float"]["int"] = "float"
ttype["<"]["float"]["int"] = "logic"
ttype[">"]["float"]["int"] = "logic"
ttype["<="]["float"]["int"] = "logic"
ttype[">="]["float"]["int"] = "logic"
ttype["=="]["float"]["int"] = "logic"
ttype["!="]["float"]["int"] = "logic"

ttype["+"]["float"]["float"] = "float"
ttype["-"]["float"]["float"] = "float"
ttype["*"]["float"]["float"] = "float"
ttype["/"]["float"]["float"] = "float"
ttype["<"]["float"]["float"] = "logic"
ttype[">"]["float"]["float"] = "logic"
ttype["<="]["float"]["float"] = "logic"
ttype[">="]["float"]["float"] = "logic"
ttype["=="]["float"]["float"] = "logic"
ttype["!="]["float"]["float"] = "logic"

ttype["+"]["vector"]["vector"] = "vector"
ttype["-"]["vector"]["vector"] = "vector"
ttype["*"]["vector"]["vector"] = "vector"
ttype["/"]["vector"]["vector"] = "vector"
ttype["+="]["vector"]["vector"] = "vector"
ttype["-="]["vector"]["vector"] = "vector"
ttype["*="]["vector"]["vector"] = "vector"
ttype["/="]["vector"]["vector"] = "vector"

ttype[".+"]["vector"]["vector"] = "vector"
ttype[".+"]["vector"]["int"] = "vector"
ttype[".+"]["vector"]["float"] = "vector"
ttype[".+"]["int"]["vector"] = "vector"
ttype[".+"]["float"]["vector"] = "vector"

ttype[".-"]["vector"]["vector"] = "vector"
ttype[".-"]["vector"]["int"] = "vector"
ttype[".-"]["vector"]["float"] = "vector"
ttype[".-"]["int"]["vector"] = "vector"
ttype[".-"]["float"]["vector"] = "vector"

ttype[".*"]["vector"]["vector"] = "vector"
ttype[".*"]["vector"]["int"] = "vector"
ttype[".*"]["vector"]["float"] = "vector"
ttype[".*"]["int"]["vector"] = "vector"
ttype[".*"]["float"]["vector"] = "vector"

ttype["./"]["vector"]["vector"] = "vector"
ttype["./"]["vector"]["int"] = "vector"
ttype["./"]["vector"]["float"] = "vector"
ttype["./"]["int"]["vector"] = "vector"
ttype["./"]["float"]["vector"] = "vector"

ttype["'"]["vector"][None] = "vector"
ttype["-"]["vector"][None] = "vector"
ttype["-"]["int"][None] = "int"
ttype["-"]["float"][None] = "float"
ttype["+"]["string"]["string"] = "string"


class NodeVisitor(object):
    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        print("Gen visit: " + node.__class__.__name__ + ": " + str(node))
        #if isinstance(node, list):
        #    for elem in node:
        #        self.visit(elem)
        #else:
        #    for child in node.children:
        #        if isinstance(child, list):
        #            for item in child:
        #                if isinstance(item, AST.Node):
        #                    self.visit(item)
        #        elif isinstance(child, AST.Node):
        #            self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.table = SymbolTable(None, "Program")
        self.loop_iterator = 0

    def visitProgram(self, node):
        self.visit(node.lines)

    def visitLines(self, node):
        self.visit(node.line)

    def visitPrint(self, node):
        if node.expr is not None: self.visit(node.expr)

    def visitReturn(self, node):
        if node.expr is not None: self.visit(node.expr)

    def visitBreak(self, node):
        if not self.loop_iterator > 0:
            print("Line {}: BREAK outside loop function".format(node.line))

    def visitReturn(self, node):
        pass

    def visitReturn(self, node):
        pass

    def visitReturn(self, node):
        pass

    def visitReturn(self, node):
        pass

    def visitReturn(self, node):
        pass

    def visitReturn(self, node):
        pass

    def visitReturn(self, node):
        pass

    def visitReturn(self, node):
        pass

    def visitReturn(self, node):
        pass

    def visitReturn(self, node):
        pass

    def visitReturn(self, node):
        pass

    def visitReturn(self, node):
        pass

    def visitReturn(self, node):
        pass

    def visitReturn(self, node):
        pass


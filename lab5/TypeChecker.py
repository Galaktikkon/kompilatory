from AST import *
from ast import AST
from operations import *
from SymbolTable import SymbolTable

ttype = {}

ttype["'", Matrix] = Matrix


ttype["-", Int] = Int
ttype["-", Float] = Float
ttype["-", Vector] = Vector
ttype["-", Matrix] = Matrix


ttype["*", Int, Int] = Int
ttype["*", Float, Float] = Float
ttype["*", Int, Float] = Float
ttype["*", Float, Int] = Float

ttype["*", Int, Vector] = Vector
ttype["*", Vector, Int] = Vector
ttype["*", Float, Vector] = Vector
ttype["*", Vector, Float] = Vector

ttype["*", Int, Matrix] = Matrix
ttype["*", Matrix, Int] = Matrix
ttype["*", Float, Matrix] = Matrix
ttype["*", Matrix, Float] = Matrix

ttype["*", Matrix, Matrix] = Matrix

ttype["*", Int, String] = String
ttype["*", String, Int] = String


ttype["/", Int, Int] = Float
ttype["/", Float, Float] = Float
ttype["/", Int, Float] = Float
ttype["/", Float, Int] = Float

ttype["/", Int, Vector] = Vector
ttype["/", Vector, Int] = Vector
ttype["/", Float, Vector] = Vector
ttype["/", Vector, Float] = Vector

ttype["/", Int, Matrix] = Matrix
ttype["/", Matrix, Int] = Matrix
ttype["/", Float, Matrix] = Matrix
ttype["/", Matrix, Float] = Matrix


ttype[".*", Vector, Vector] = Vector
ttype[".*", Matrix, Matrix] = Matrix

ttype["./", Vector, Vector] = Vector
ttype["./", Matrix, Matrix] = Matrix


ttype["+", Int, Int] = Int
ttype["+", Float, Float] = Float
ttype["+", Int, Float] = Float
ttype["+", Float, Int] = Float
ttype["+", String, String] = String


ttype["-", Int, Int] = Int
ttype["-", Float, Float] = Float
ttype["-", Int, Float] = Float
ttype["-", Float, Int] = Float


ttype[".+", Vector, Vector] = Vector
ttype[".+", Matrix, Matrix] = Matrix

ttype[".-", Vector, Vector] = Vector
ttype[".-", Matrix, Matrix] = Matrix


ttype["==", Vector, Vector] = Bool
ttype["==", Matrix, Matrix] = Bool
ttype["==", Int, Int] = Bool
ttype["==", Float, Float] = Bool
ttype["==", Int, Float] = Bool
ttype["==", Float, Int] = Bool
ttype["==", String, String] = Bool

ttype["!=", Vector, Vector] = Bool
ttype["!=", Matrix, Matrix] = Bool
ttype["!=", Int, Int] = Bool
ttype["!=", Float, Float] = Bool
ttype["!=", Int, Float] = Bool
ttype["!=", Float, Int] = Bool
ttype["!=", String, String] = Bool

ttype["<", Int, Int] = Bool
ttype["<", Float, Float] = Bool
ttype["<", Int, Float] = Bool
ttype["<", Float, Int] = Bool
ttype["<", String, String] = Bool

ttype[">", Int, Int] = Bool
ttype[">", Float, Float] = Bool
ttype[">", Int, Float] = Bool
ttype[">", Float, Int] = Bool
ttype[">", String, String] = Bool

ttype["<=", Int, Int] = Bool
ttype["<=", Float, Float] = Bool
ttype["<=", Int, Float] = Bool
ttype["<=", Float, Int] = Bool
ttype["<=", String, String] = Bool

ttype[">=", Int, Int] = Bool
ttype[">=", Float, Float] = Bool
ttype[">=", Int, Float] = Bool
ttype[">=", Float, Int] = Bool
ttype[">=", String, String] = Bool


class NodeVisitor(object):
    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(
        self, node
    ):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable(None, "Program")
        self.error_list = []

    def visit_Program(self, node):
        self.visit(node.lines)

    def visit_Lines(self, node):
        current = node
        while current is not None:
            self.visit(current.line)
            current = current.lines

    def visit_Print(self, node):
        self.visit(node.expr)

    def visit_Return(self, node):
        self.visit(node.expr)

    def visit_Break(self, node):
        pass

    def visit_Continue(self, node):
        pass

    def visit_Assignment(self, node):
        expr_type = self.visit(node.expr)
        self.symbol_table.put(node.variable.identifier, expr_type)

    def visit_IfElse(self, node):
        cond_type = self.visit(node.condition)
        if cond_type is Bool:
            self.visit(node.if_branch)
            self.visit(node.else_branch)
        else:
            self.error_list.append(f"(IfElse): Type Error at line: {node.line_number}")

    def visit_BinOp(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)
        if not (node.op, type_left, type_right) in ttype:
            self.error_list.append(f"(BinOp): Type Error at line: {node.line_number}")
        else:
            return ttype[node.op, type_left, type_right]

    def visit_ForLoop(self, node):
        self.visit(node.variable)
        for_scope: SymbolTable = self.symbol_table.pushScope("for scope")
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)
        if start_type is Int and end_type is Int:
            for_scope.put(node.variable.identifier, Int)
        self.visit(node.body)

    def visit_WhileLoop(self, node):
        cond_type = self.visit(node.condition)
        if cond_type is Bool:
            self.visit(node.body)

    def visit_Vector(self, node):
        return self.visit(node.vector_elements)

    def visit_VectorList(self, node):
        pass

    def visit_Matrix(self, node):
        vector_types = set()
        vector_sizes = set()
        rows = 0
        vector_list = node.vectors
        current = vector_list
        while current is not None:
            if type(current) is VectorList:
                vector = self.visit(current.vector)
                current = current.vectors
            else:
                vector = self.visit(current)
                current = None
            vector_types.add(vector.inner_type)
            vector_sizes.add(vector.size)
            rows += 1
        if len(vector_types) == 1 and len(vector_sizes) == 1:
            print(vector_types, vector_sizes, rows)
            return Matrix(
                inner_type=vector_types.pop(), shape=(rows, vector_sizes.pop())
            )
        else:
            self.error_list.append(f"(Matrix): Type Error at line: {node.line_number}")

    def visit_MatrixOp(self, node):
        enumerable1 = self.visit(node.enumerable1)
        if node.enumerable2:
            enumerable2 = self.visit(node.enumerable2)
            if enumerable1 is Int and enumerable2 is Int:
                return Matrix(Int, (None, None))
        if enumerable1 is Int:
            return Matrix(Int, (None, None))

        self.error_list.append(f"(MatrixOp): Type Error at line: {node.line_number}")

    def visit_String(self, node):
        return String

    def visit_FloatNum(self, node):
        return Float

    def visit_IntNum(self, node):
        return Int

    def visit_LValue(self, node):
        return self.symbol_table.get(node.identifier)

    def visit_RefValue(self, node):
        identifier_type = self.symbol_table.get(node.identifier)
        if identifier_type is Vector:
            self.visit(node.row)
        if identifier_type is Vector and node.col:
            self.error_list.append(
                f"(RefValue): Type Error at line: {node.line_number}"
            )
        if identifier_type is Matrix:
            self.visit(node.row)
            self.visit(node.col)
        else:
            self.error_list.append(
                f"(RefValue): Type Error at line: {node.line_number}"
            )
        return identifier_type

    def visit_ElementsList(self, node):
        elements_types = set()
        current = node.element_list
        count = 1
        while current is not None:
            elements_types.add(self.visit(current.element))
            current = current.element_list
            count += 1
        if len(elements_types) == 1:
            return Vector(elements_types.pop(), count)
        else:
            self.error_list.append(
                f"(ElementsList): Type Error at line: {node.line_number}"
            )
            return Vector(None, None)

    def visit_Transpose(self, node):
        operand_type = self.visit(node.identifier)
        return ttype["'", operand_type]

    def visit_UnaryOp(self, node):
        operand_type = self.visit(node.operand)
        return ttype[node.operator, operand_type]

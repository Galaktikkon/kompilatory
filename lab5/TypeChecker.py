from AST import *
from ast import AST
from expression_results import *
from SymbolTable import SymbolTable
from errors import SemanticError

WHILE_SCOPE = "while_scope"
FOR_SCOPE = "for_scope"
BLOCK_SCOPE = "block_scope"


class NodeVisitor(object):
    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        print("Gen visit: " + node + ": " + str(node))


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

        scope = self.symbol_table.name
        if not (scope == FOR_SCOPE or scope == WHILE_SCOPE):
            self.error_list.append(
                SemanticError(
                    text=f"'break' statement used out of loop statement",
                    line_number=node.line_number,
                )
            )

    def visit_Continue(self, node):
        scope = self.symbol_table.name
        if not (scope == FOR_SCOPE or scope == WHILE_SCOPE):
            self.error_list.append(
                SemanticError(
                    text=f"'continue' statement used out of loop statement",
                    line_number=node.line_number,
                )
            )

    def visit_Assignment(self, node):
        expr_type = self.visit(node.expr)
        self.symbol_table.put(node.variable.identifier, expr_type)

    def visit_IfElse(self, node):
        cond_type = self.visit(node.condition)
        if cond_type is Bool:
            self.visit(node.if_branch)
            if node.else_branch:
                self.visit(node.else_branch)
        else:
            self.error_list.append(
                SemanticError(
                    text=f"{node.condition} is cannot be interpreted as 'Bool' type",
                    line_number=node.line_number,
                )
            )

    def visit_BinOp(self, node):
        type_left = self.visit(node.left)
        type_right = self.visit(node.right)

        result = result_type(node.op, type_left, type_right)

        if not result:
            self.error_list.append(
                SemanticError(
                    text=f"'{node.op}' is not supported between instances of '{type_left}' and '{type_right}'",
                    line_number=node.line_number,
                )
            )
        else:
            return result_type(node.op, type_left, type_right)

    def visit_ForLoop(self, node):
        self.symbol_table = self.symbol_table.pushScope(FOR_SCOPE)
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)
        if start_type is Int and end_type is Int:
            self.symbol_table.put(node.variable, Int)
        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()

    def visit_WhileLoop(self, node):
        cond_type = self.visit(node.condition)
        self.symbol_table = self.symbol_table.pushScope(WHILE_SCOPE)
        if cond_type is Bool:
            self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()

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

        if not len(vector_types) == 1:
            self.error_list.append(
                SemanticError(
                    text=f"Matrix vector elements are not of the same type",
                    line_number=node.line_number,
                )
            )
            return

        if not len(vector_sizes) == 1:
            self.error_list.append(
                SemanticError(
                    text=f"Matrix vectors are not of the same size",
                    line_number=node.line_number,
                )
            )
            return
        return Matrix(inner_type=vector_types.pop(), shape=(rows, vector_sizes.pop()))

    def visit_MatrixOp(self, node):
        enumerable1 = self.visit(node.enumerable1)
        value1 = (
            node.enumerable1.value
            if type(node.enumerable1) is IntNum
            else node.enumerable1.identifier
        )
        if node.enumerable2:
            enumerable2 = self.visit(node.enumerable2)
            if not enumerable1 is Int:
                self.error_list.append(
                    SemanticError(
                        text=f"First dimension is not type of {Int}",
                        line_number=node.line_number,
                    )
                )
                return
            if not enumerable2 is Int:
                self.error_list.append(
                    SemanticError(
                        text=f"Second dimension is not type of {Int}",
                        line_number=node.line_number,
                    )
                )
                return
            else:
                value2 = (
                    node.enumerable2.value
                    if type(node.enumerable2) is IntNum
                    else node.enumerable2.identifier
                )
                return Matrix(Int, (value1, value2))

        if not enumerable1 is Int:
            self.error_list.append(
                SemanticError(
                    text=f"First dimension is not type of {Int}",
                    line_number=node.line_number,
                )
            )
            return
        else:
            return Matrix(Int, (value1, value1))

    def visit_String(self, node):
        return String

    def visit_FloatNum(self, node):
        return Float

    def visit_IntNum(self, node):
        return Int

    def visit_LValue(self, node):
        return self.symbol_table.get(node.identifier)

    def visit_RefValue(self, node):
        identifier = self.symbol_table.get(node.identifier)

        if not identifier:
            self.error_list.append(
                SemanticError(
                    text=f"'{node.identifier}' is not defined",
                    line_number=node.line_number,
                )
            )
            return

        if not (type(identifier) is Matrix or type(identifier) is Vector):
            self.error_list.append(
                SemanticError(
                    text=f"'{node.identifier}' is expected to be type of Vector or Matrix",
                    line_number=node.line_number,
                )
            )
            return
        if type(identifier) is Vector:
            n = identifier.size
            if not 0 <= int(node.row.value) < int(n):
                self.error_list.append(
                    SemanticError(
                        text=f"index {node.row.value} out of bounds of {identifier}",
                        line_number=node.line_number,
                    )
                )
            else:
                self.visit(node.row)

        if type(identifier) is Vector and node.col:

            self.error_list.append(
                SemanticError(
                    text=f"column index is out of bounds for type Vector",
                    line_number=node.line_number,
                )
            )

        if type(identifier) is Matrix:
            n, m = identifier.shape
            if n == None and m == None:
                pass
            else:
                if type(node.col) is IntNum and not 0 <= int(node.col.value) < int(m):
                    self.error_list.append(
                        SemanticError(
                            text=f"index {node.col.value} out of bounds of {identifier}",
                            line_number=node.line_number,
                        )
                    )
                    return
                if type(node.row) is IntNum and not 0 <= int(node.row.value) < int(n):
                    self.error_list.append(
                        SemanticError(
                            text=f"index {node.row.value} out of bounds of {identifier}",
                            line_number=node.line_number,
                        )
                    )
                    return
                else:
                    self.visit(node.row)
                    self.visit(node.col)

        return identifier

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
                SemanticError(
                    text=f"Vector elements are not of the same type",
                    line_number=node.line_number,
                )
            )
            return Vector(None, None)

    def visit_Transpose(self, node):
        operand = self.symbol_table.get(node.identifier)
        return result_type("'", operand)

    def visit_UnaryOp(self, node):
        operand_type = self.visit(node.operand)
        return result_type(node.operator, operand_type)

    def visit_Block(self, node):

        scope_name = self.symbol_table.name

        if scope_name == WHILE_SCOPE or scope_name == FOR_SCOPE:
            self.visit(node.lines)
        else:
            self.symbol_table = self.symbol_table.pushScope(BLOCK_SCOPE)
            self.visit(node.lines)
            self.symbol_table = self.symbol_table.popScope()

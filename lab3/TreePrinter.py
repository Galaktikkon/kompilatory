import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


def print_with_indent(indent, msg):
    print(f"{'|  ' * indent}{msg}")


class TreePrinter:
    @addToClass(AST.Node)
    def print_tree(self, indent=0):
        raise NotImplementedError("printTree not implemented for this class")

    @addToClass(AST.Lines)
    def print_tree(self, indent=0):
        if self.lines:
            self.lines.print_tree(indent)
        self.line.print_tree(indent)

    @addToClass(AST.Print)
    def print_tree(self, indent=0):
        print_with_indent(indent, "PRINT")
        self.expr.print_tree(indent + 1)

    @addToClass(AST.Return)
    def print_tree(self, indent=0):
        print_with_indent(indent, "RETURN")
        self.expr.print_tree(indent + 1)

    @addToClass(AST.Break)
    def print_tree(self, indent=0):
        print_with_indent(indent, "BREAK")

    @addToClass(AST.Continue)
    def print_tree(self, indent=0):
        print_with_indent(indent, "CONTINUE")

    @addToClass(AST.Assignment)
    def print_tree(self, indent=0):
        print_with_indent(indent, str(self.op))
        self.variable.print_tree(indent + 1)
        self.expr.print_tree(indent + 1)

    @addToClass(AST.IfElse)
    def print_tree(self, indent=0):
        print_with_indent(indent, "IF")
        self.condition.print_tree(indent + 1)
        print_with_indent(indent, "THEN")
        self.if_branch.print_tree(indent + 1)
        if self.else_branch:
            print_with_indent(indent, "ELSE")
            self.else_branch.print_tree(indent + 1)

    @addToClass(AST.BinOp)
    def print_tree(self, indent=0):
        print_with_indent(indent, str(self.op))
        self.left.print_tree(indent + 1)
        self.right.print_tree(indent + 1)

    @addToClass(AST.ForLoop)
    def print_tree(self, indent=0):
        print_with_indent(indent, "FOR")
        print_with_indent(indent + 1, str(self.variable))
        print_with_indent(indent + 1, "RANGE")
        self.start.print_tree(indent + 2)
        self.end.print_tree(indent + 2)
        self.body.print_tree(indent + 1)

    @addToClass(AST.WhileLoop)
    def print_tree(self, indent=0):
        print_with_indent(indent, "WHILE")
        self.condition.print_tree(indent + 1)
        self.body.print_tree(indent + 1)

    @addToClass(AST.Vector)
    def print_tree(self, indent=0):
        print_with_indent(indent, "VECTOR")
        self.vector.print_tree(indent + 1)

    @addToClass(AST.VectorList)
    def print_tree(self, indent=0):
        if self.vectors:
            self.vectors.print_tree(indent)
            print_with_indent(indent, "VECTOR")
        self.vector.print_tree(indent + 1)

    @addToClass(AST.Matrix)
    def print_tree(self, indent=0):
        print_with_indent(indent, "VECTOR")
        self.vectors.print_tree(indent + 1)

    @addToClass(AST.MatrixOp)
    def print_tree(self, indent=0):
        print_with_indent(indent, str(self.type))
        self.enumerable.print_tree(indent + 1)

    @addToClass(AST.String)
    def print_tree(self, indent=0):
        print_with_indent(indent, str(self.value))

    @addToClass(AST.FloatNum)
    def print_tree(self, indent=0):
        print_with_indent(indent, str(self.value))

    @addToClass(AST.IntNum)
    def print_tree(self, indent=0):
        print_with_indent(indent, str(self.value))

    @addToClass(AST.LValue)
    def print_tree(self, indent=0):
        print_with_indent(indent, str(self.identifier))
        if self.enum_list:
            self.enum_list.print_tree(indent)

    @addToClass(AST.RefValue)
    def print_tree(self, indent=0):
        print_with_indent(indent, "REF")
        print_with_indent(indent + 1, str(self.identifier))
        self.ref.print_tree(indent + 1)

    @addToClass(AST.ElementsList)
    def print_tree(self, indent=0):
        self.enumerable.print_tree(indent)
        if self.enum_list:
            self.enum_list.print_tree(indent)

    @addToClass(AST.EnumerableList)
    def print_tree(self, indent=0):
        self.enumerable.print_tree(indent)
        if self.enum_list:
            self.enum_list.print_tree(indent)

    @addToClass(AST.Transpose)
    def print_tree(self, indent=0):
        print_with_indent(indent, "TRANSPOSE")
        print_with_indent(indent + 1, str(self.identifier))

    @addToClass(AST.UnaryOp)
    def print_tree(self, indent=0):
        print_with_indent(indent, str(self.op))
        self.operand.print_tree(indent + 1)

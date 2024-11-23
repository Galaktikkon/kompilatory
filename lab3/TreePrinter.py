import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


def print_with_indent(indent, msg):
    print(f"{'|\t' * indent}{msg}")


class TreePrinter:
    @addToClass(AST.Node)
    def print_tree(self, indent=0):
        raise NotImplementedError("printTree not implemented for this class")

    @addToClass(AST.BinOp)
    def print_tree(self, indent=0):
        print_with_indent(indent, str(self.op))
        self.left.print_tree(indent + 1)
        self.right.print_tree(indent + 1)

    @addToClass(AST.UnaryOp)
    def print_tree(self, indent=0):
        print_with_indent(indent, str(self.op))
        self.operand.print_tree(indent + 1)

    @addToClass(AST.Assignment)
    def print_tree(self, indent=0):
        print_with_indent(indent, str(self.op))
        self.variable.print_tree(indent + 1)
        self.expr.print_tree(indent + 1)

    @addToClass(AST.IfElse)
    def print_tree(self, indent=0):
        print_with_indent(indent, "IF")
        self.condition.printTree(indent + 1)
        print_with_indent(indent, "THEN")
        self.if_branch.printTree(indent + 1)
        print_with_indent(indent, "ELSE")
        self.else_branch.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def print_tree(self, indent=0):
        print_with_indent(indent, "FOR")
        print_with_indent(indent + 1, str(self.variable.name))
        print_with_indent(indent + 1, "RANGE")
        self.start.print_tree(indent + 2)
        self.end.print_tree(indent + 2)
        self.body.print_tree(indent + 1)

    @addToClass(AST.WhileLoop)
    def print_tree(self, indent=0):
        print_with_indent(indent, "WHILE")
        self.condition.print_tree(indent + 1)
        self.body.print_tree(indent + 1)

    @addToClass(AST.Block)
    def print_tree(self, indent=0):
        pass

    @addToClass(AST.Break)
    def print_tree(self, indent=0):
        print_with_indent(indent, "BREAK")

    @addToClass(AST.Continue)
    def print_tree(self, indent=0):
        print_with_indent(indent, "CONTINUE")

    @addToClass(AST.Return)
    def print_tree(self, indent=0):
        print_with_indent(indent, "RETURN")
        self.expr.print_tree(indent + 1)

    @addToClass(AST.Print)
    def print_tree(self, indent=0):
        print_with_indent(indent, "PRINT")
        self.expr.print_tree(indent + 1)

    @addToClass(AST.Vector)
    def print_tree(self, indent=0):
        pass

    @addToClass(AST.Transpose)
    def print_tree(self, indent=0):
        pass

    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

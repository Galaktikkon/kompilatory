import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    @addToClass(AST.IntLiteral)
    @addToClass(AST.FloatLiteral)
    @addToClass(AST.StringLiteral)
    @addToClass(AST.Variable)
    @addToClass(AST.BinOp)
    @addToClass(AST.UnaryOp)
    @addToClass(AST.Assignment)
    @addToClass(AST.IfElse)
    @addToClass(AST.ForLoop)
    @addToClass(AST.WhileLoop)
    @addToClass(AST.Block)
    @addToClass(AST.Break)
    @addToClass(AST.Continue)
    @addToClass(AST.Return)
    @addToClass(AST.Print)
    @addToClass(AST.MatrixOp)
    @addToClass(AST.Vector)
    @addToClass(AST.Transpose)
    @addToClass(AST.Condition)

    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)
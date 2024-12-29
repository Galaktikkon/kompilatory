class SymbolTable(object):
    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.table = {}

    #

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.table[name] = symbol

    #

    def get(self, name):  # get variable symbol or fundef from <name> entry
        return self.table.get(name, self.__get_from_parent(name))

    def __get_from_parent(self, name):
        parent_scope = self.getParentScope()
        if parent_scope:
            return parent_scope.get(name)

    #

    def getParentScope(self):
        return self.parent

    #

    def pushScope(self, name):
        return SymbolTable(self, name)

    #

    def popScope(self):
        return self.parent

    #
    def __repr__(self):
        return str(self.table)

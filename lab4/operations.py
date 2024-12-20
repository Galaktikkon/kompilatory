from typing import Union


class Int:
    def __hash__(self):
        return hash(Int)

    def __str__(self):
        return "Int"

    def __repr__(self):
        return "Int"


class Float:
    def __hash__(self):
        return hash(Float)

    def __repr__(self):
        return "Float"

    def __str__(self):
        return "Float"


class Bool:
    def __hash__(self):
        return hash(Bool)

    def __repr__(self):
        return "Bool"

    def __str__(self):
        return "Bool"


class String:
    def __hash__(self):
        return hash(String)

    def __repr__(self):
        return "String"

    def __str__(self):
        return "String"


class Vector:
    def __init__(self, inner_type, size):
        self.inner_type = inner_type
        self.size = size

    def __hash__(self):
        return hash(Vector)

    def __repr__(self):
        return f"Vector({self.inner_type}, {self.size})"

    def __str__(self):
        return f"Vector({self.inner_type}, {self.size})"


class Matrix:
    def __init__(self, inner_type, shape):
        self.inner_type = inner_type
        self.shape = shape

    def __hash__(self):
        return hash(Matrix)

    def __repr__(self):
        return f"Matrix({self.inner_type}, {self.shape})"

    def __str__(self):
        return f"Matrix({self.inner_type}, {self.shape})"

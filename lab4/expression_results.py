class MetaClass(type):
    def __hash__(cls):
        return hash(cls.__name__)

    def __repr__(cls):
        return cls.__name__

    def __str__(cls):
        return cls.__name__


class Int(metaclass=MetaClass):
    pass


class Float(metaclass=MetaClass):
    pass


class Bool(metaclass=MetaClass):
    pass


class String(metaclass=MetaClass):
    pass


class Vector(metaclass=MetaClass):
    def __init__(self, inner_type, size):
        self.inner_type = inner_type
        self.size = size

    def __repr__(self):
        return f"Vector({self.inner_type}, {self.size})"

    def __str__(self):
        return f"Vector({self.inner_type}, {self.size})"


class Matrix(metaclass=MetaClass):
    def __init__(self, inner_type, shape):
        self.inner_type = inner_type
        self.shape = shape

    def __repr__(self):
        return f"Matrix({self.inner_type}, {self.shape})"

    def __str__(self):
        return f"Matrix({self.inner_type}, {self.shape})"


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


def get_result_domain(left, right):
    return Float if left == Float or right == Float else Int


def result_type(op, left, right=None):

    match op:

        case "'":
            return Matrix(left.inner_type, (left.shape[1], left.shape[0]))

        case "-" if type(left) is Matrix or type(left) is Vector:
            return left

        case "*" if type(left) is Matrix and type(right) is Matrix:

            if left.shape[1] != right.shape[0]:
                return None
            result_domain = get_result_domain(left.inner_type, right.inner_type)
            return Matrix(result_domain, (left.shape[0], right.shape[1]))

        case "*" if type(left) is Matrix and type(right) is Vector:
            if left.shape[1] != right.size:
                return None

            result_domain = get_result_domain(left.inner_type, right.inner_type)
            return Matrix(result_domain, (left.shape[0], 1))

        case "*" if type(left) is Vector and type(right) is Matrix:
            if left.size != right.shape[0]:
                return None

            result_domain = get_result_domain(left.inner_type, right.inner_type)
            return Vector(result_domain, right.shape[1])

        case "*" | "/":
            if (type(left) is Vector or type(left) is Matrix) and right is Int:
                return left

            if left is Int and (type(right) is Vector or type(right) is Matrix):
                return right

            if (type(left) is Vector or type(left) is Matrix) and right is Float:
                left.inner_type = get_result_domain(left.inner_type, right)
                return left

            if left is Float and (type(right) is Vector or type(right) is Matrix):
                right.inner_type = get_result_domain(left, right.inner_type)
                return right

        case ".+" | ".-" | ".*" | "./":
            if type(left) is Matrix and type(right) is Matrix:
                if left.shape != right.shape:
                    return None
                result_domain = get_result_domain(left.inner_type, right.inner_type)
                return Matrix(result_domain, left)

            elif type(left) is Vector and type(right) is Vector:
                if left.size != right.size:
                    return None
                result_domain = get_result_domain(left.inner_type, right.inner_type)
                return Matrix(result_domain, left)

        case _:
            if right:
                if (op, left, right) in ttype:
                    return ttype[op, left, right]
            else:
                if (op, left) in ttype:
                    return ttype[op, left]
            return None

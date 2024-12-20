import sys
from sly import Lexer


class Scanner(Lexer):

    error_list = []

    tokens = {
        ID,
        MAT_PLUS,
        MAT_MINUS,
        MAT_MUL,
        MAT_DIV,
        ADD_ASSIGN,
        SUB_ASSIGN,
        MUL_ASSIGN,
        DIV_ASSIGN,
        LEQ,
        GEQ,
        EQ,
        NEQ,
        FLOAT,
        INT,
        STR,
        IF,
        ELSE,
        FOR,
        WHILE,
        BREAK,
        CONTINUE,
        RETURN,
        EYE,
        ZEROS,
        ONES,
        PRINT,
    }

    # Literals
    literals = {
        "+",
        "-",
        "*",
        "/",
        "=",
        ">",
        "<",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        ",",
        ":",
        ";",
        "'",
    }

    # String containing ignored characters (between tokens)
    ignore = " \t"

    # Ignore comments
    ignore_comment = r"\#.*"

    # Define a rule so we can track line numbers
    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    # Base ID rule
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"

    # Special cases
    ID["if"] = IF
    ID["else"] = ELSE
    ID["for"] = FOR
    ID["while"] = WHILE
    ID["break"] = BREAK
    ID["continue"] = CONTINUE
    ID["return"] = RETURN
    ID["eye"] = EYE
    ID["zeros"] = ZEROS
    ID["ones"] = ONES
    ID["print"] = PRINT

    # Matrix operators
    MAT_PLUS = r"\.\+"
    MAT_MINUS = r"\.-"
    MAT_MUL = r"\.\*"
    MAT_DIV = r"\./"

    # Assign operators
    ADD_ASSIGN = r"\+="
    SUB_ASSIGN = r"-="
    MUL_ASSIGN = r"\*="
    DIV_ASSIGN = r"/="

    # Comparison operators
    LEQ = r"<="
    GEQ = r">="
    EQ = r"=="
    NEQ = r"!="

    # Strings
    STR = r"\"([^\"\\\n\r]|\\.)*\""

    # Floats
    FLOAT = r"(\d+\.\d*|\d*\.\d+|0\.)((E|e)(-|\+)?([1-9]\d*|0))?"

    # Integers
    INT = r"0|[1-9]\d*"

    # Error handling rule for illegal characters
    def error(self, t):
        Scanner.error_list.append(f"({self.lineno}): Illegal character: '{t.value[0]}'")
        print(f"({self.lineno}): Illegal character: '{t.value[0]}'")
        self.index += 1


if __name__ == "__main__":

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples\\example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()

    for tok in lexer.tokenize(text):
        print(f"({tok.lineno}): {tok.type} ('{tok.value}')")

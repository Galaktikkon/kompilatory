class Error:
    def __init__(self, text, line_number):
        self.text = text
        self.line_number = line_number


class SemanticError(Error):
    def __init__(self, text, line_number):
        super().__init__(text, line_number)

    def __repr__(self):
        return f"\033[35m{self.line_number}: {self.text} \033[0m"


class ParserError(Error):
    def __init__(self, text, line_number):
        super().__init__(text, line_number)

    def __repr__(self):
        return f"\033[36m{self.line_number}: {self.text} \033[0m"


class LexerError(Error):
    def __init__(self, text, line_number):
        super().__init__(text, line_number)

    def __repr__(self):
        return f"\033[32m{self.line_number}: {self.text} \033[0m"

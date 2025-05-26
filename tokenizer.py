import re

# List of reserved keywords for the language
RESERVED_KEYWORDS = [
    "let", "in", "within", "where", "fn", "aug", "and", "or", "not",
    "gr", "ge", "ls", "le", "eq", "ne", "true", "false", "nil", "dummy", "rec"
]

# Check if a token is a reserved keyword
def isReservedKeyword(token):
    return token in RESERVED_KEYWORDS

# Check if an element is a valid ID
def isID(element):
    return re.match(r'^[A-Za-z][A-Za-z0-9_]*', element)

# Check if an element is an INT
def isDigit(element):
    return re.match(r'^[0-9]+', element)

# Check if an element is a string (single-quoted)
def isString(element):
    return re.match(r"^'([^'\\]|\\.)*'", element)  # Handle escaped quotes

# Check if an element is a double operator (two characters)
def isDoubleOperator(element):
    # RPAL-specific double operators based on the grammar
    double_ops = ['>=', '<=', '->', '**']
    for op in double_ops:
        if element.startswith(op):
            return re.match(re.escape(op), element)
    return None

# Check if an element is an operator (single character)
def isOperator(element):
    # RPAL-specific single operators based on the grammar
    return re.match(r'^[+\-*/&@|><.=~$!#%^_\[\]{}"`?]', element)

# Check if an element is a punctuation character
def isPunctuation(element):
    return re.match(r'^[\(\)\;\,]', element)

# Check if an element is a comment (starts with //)
def isComment(element):
    return re.match(r"^(//.*)", element)

# Token class to represent a lexical token
class Token:
    def __init__(self, type, value, line_number):
        self.type = type
        self.value = value
        self.line_number = line_number

    def getValue(self):
        return self.value

    def getType(self):
        return self.type

    def getLineNumber(self):
        return self.line_number
    
    def __str__(self):
        return f"Token({self.type}, '{self.value}', {self.line_number})"
    
    def __repr__(self):
        return self.__str__()

# Tokenize input lines into a list of tokens
def tokenize(lines):
    """
    Tokenizes a list of source code lines into a list of Token objects.
    
    Args:
        lines (list of str): The lines of source code to tokenize.
    
    Returns:
        list: A list of Token objects.
    
    The function processes each line, removing inline comments, and iteratively 
    matches and extracts tokens in the following order:
        - Double operators (==, !=, etc.)
        - IDs and keywords
        - INTs
        - Strings
        - Single operators
        - Punctuation
    
    Each token is annotated with its type, value, and line number.
    """
    tokens = []
    
    for line_number, line in enumerate(lines, start=1):
        # Remove inline comments
        line = line.split('//', 1)[0]

        while line:
            line = line.lstrip()  # Remove leading whitespace
            if not line:
                break

            # Check for double operators first
            match = isDoubleOperator(line)
            if match:
                tokens.append(Token("OPERATOR", match.group(), line_number))
                line = line[match.end():]
                continue

            # ID or keyword
            match = isID(line)
            if match:
                token = match.group()
                if isReservedKeyword(token):
                    tokens.append(Token("KEYWORD", token, line_number))
                else:
                    tokens.append(Token("ID", token, line_number))
                line = line[match.end():]
                continue

            # INT
            match = isDigit(line)
            if match:
                tokens.append(Token("INT", match.group(), line_number))
                line = line[match.end():]
                continue

            # String
            match = isString(line)
            if match:
                tokens.append(Token("STRING", match.group(), line_number))
                line = line[match.end():]
                continue

            # Single operator
            match = isOperator(line)
            if match:
                tokens.append(Token("OPERATOR", match.group(), line_number))
                line = line[match.end():]
                continue

            # Punctuation
            match = isPunctuation(line)
            if match:
                tokens.append(Token(match.group(), match.group(), line_number))
                line = line[match.end():]
                continue

            # If no match found, it's an unexpected character
            unexpected_char = line[0]
            print(f"Warning: Unexpected character '{unexpected_char}' at line {line_number}")
            line = line[1:]  # Skip the unexpected character

    return tokens

# Example usage and testing
# def test_lexer():
#     """Test the lexer with RPAL sample code"""
#     test_code = [
#         "let x = 42 in x + 1",
#         "fn x . x + 1",
#         "B -> Tc '|' Tc",
#         "let add = fn x y . x + y in add 5 3",
#         "x >= 10 and y <= 20",
#         "2 ** 3 * 4",
#         "// This is a comment",
#         "'Hello World' aug 'Test'",
#         "true or false",
#         "not (x gr y)"
#     ]
    
#     tokens = tokenize(test_code)
#     for token in tokens:
#         print(token)

# if __name__ == "__main__":
#     test_lexer()
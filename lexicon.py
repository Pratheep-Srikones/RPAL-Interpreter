import re

# List of reserved keywords for the language
RESERVED_KEYWORDS = [
    "let", "in", "within", "where","fn", "aug", "and", "or", "not",
    "gr", "ge", "ls", "le", "eq", "ne", "true", "false", "nil", "dummy", "rec"
]

# Check if a token is a reserved keyword
def isReservedKeyword(token):
    return token in RESERVED_KEYWORDS

# Check if an element is a valid identifier
def isIdentifier(element):
    return re.match(r'^[A-Za-z][A-Za-z0-9_]*', element)

# Check if an element is an integer
def isDigit(element):
    return re.match(r'^[0-9]+', element)

# Check if an element is a string (single-quoted)
def isString(element):
    return re.match(r"^'[^']*'", element)

# Check if an element is an operator (single character)
def isOperator(element):
    return re.match(r"^[+\-*/<>&.@/:=~|\$\[\]!\#\%\^_\{\}]", element)

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
       self.line_number = line_number #can be used to show errormessages

    def getValue(self):
       return self.value

    def getType(self):
       return self.type

    def getLineNumber(self):
       return self.line_number

# Tokenize input lines into a list of tokens
def tokenize(lines, tokens):
    for line_number, line in enumerate(lines, start=1):
       # Remove inline comments
       line = line.split('//', 1)[0]

       while line:
          line = line.lstrip()  # Remove leading whitespace
          if not line:
             break

          # Identifier or keyword
          match = isIdentifier(line)
          if match:
             token = match.group()
             if isReservedKeyword(token):
                tokens.append(Token("KEYWORD", token, line_number))
             else:
                tokens.append(Token("IDENTIFIER", token, line_number))
             line = line[match.end():]
             continue

          # Integer
          match = isDigit(line)
          if match:
             tokens.append(Token("INTEGER", match.group(), line_number))
             line = line[match.end():]
             continue

          # String
          match = isString(line)
          if match:
             tokens.append(Token("STRING", match.group(), line_number))
             line = line[match.end():]
             continue

          # Operator (single-char only)
          match = isOperator(line)
          if match:
             tokens.append(Token("OPERATOR", match.group(), line_number))
             line = line[match.end():]
             continue

          # Punctuation
          match = isPunctuation(line)
          if match:
             tokens.append(Token("PUNCTUATION", match.group(), line_number))
             line = line[match.end():]
             continue

          # Unknown token (skip with warning)
          print(f"Unrecognized token at line {line_number}: '{line[0]}'")
          line = line[1:]

    return tokens

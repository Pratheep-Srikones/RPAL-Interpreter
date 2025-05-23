#thisis a function skeleton need to define AST building mechanism and AST nodes
import RPALException


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.stack = []

    def checkToken(self, expected_type, expected_value):
        """
        Checks if the current token matches the expected type and value.
        Returns True if it matches, False otherwise.
        """
        # if self.current_token is None:
        #     raise RPALException("Unexpected end of input")
        # if self.current_token.getType() != expected_type:
        #     raise RPALException(f"Expected token type {expected_type}, got {self.current_token.getType()}")
        # if self.current_token.getValue() != expected_value:
        #     raise RPALException(f"Expected token value '{expected_value}', got '{self.current_token.getValue()}'")
        #can throw exceptions here or save itfor later(preferred)
        if self.current_token is None:
            return False
        if self.current_token.getType() != expected_type:
            return False
        if self.current_token.getValue() != expected_value:
            return False	
        return True
    def nextToken(self):
        if len(self.tokens) > 0:
            self.current_token = self.tokens.pop(0)


    

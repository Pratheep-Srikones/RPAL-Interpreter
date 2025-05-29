from Exception.RPALException import RPALException
from Tokenizer.tokenizer import Token

class Environment:
    """
    Represents an environment for variable bindings, supporting nested (parent) environments.
    Used for variable lookup and scope management in an interpreter.
    """

    def __init__(self, number, parent=None, variables=None):
        """
        Initialize a new Environment.

        Args:
            number (int): Unique identifier for the environment.
            parent (Environment, optional): Reference to the parent environment. Defaults to None.
            variables (dict, optional): Dictionary of variable bindings. Defaults to empty dict.
        """
        self.parent = parent  # Reference to the parent environment (for nested scopes)
        self.variables = variables if variables is not None else {}  # Variable bindings in this environment
        self.number = number  # Unique identifier for this environment

    def lookUpValue(self, name, line=0):
        """
        Look up the value of a variable or token in the environment chain.

        Args:
            name (str or Token): The variable name or Token to look up.

        Returns:
            The value associated with the variable or token.

        Raises:
            RPALException: If the identifier is not found in any environment.
        """
        #print(f"Looking up value for: {name} in environment {self.number}")
        
        # If name is a Token, extract its line number and value
        if type(name) is Token:
            if name.getType() == "INT":
                # If the token is an integer, return its integer value directly
                return int(name.getValue())
            if name.getType() == "STRING":
                # If the token is a string, return its string value directly
                return name.getValue()
            
            line = name.getLineNumber()
            name = name.getValue()
        # Check if the name exists in the current environment
        if name in self.variables:
            #print(f"Found {name} in environment {self.number}")
            return self.variables[name]
        # If not found in the current environment, check the parent environment recursively
        elif self.parent is not None:
            return self.parent.lookUpValue(name,line)
        # If not found in any environment, raise an exception with the line number
        else:
            raise RPALException(f"Undeclared Identifier <{name}> in line {line}")
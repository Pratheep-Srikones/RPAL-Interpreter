from RPALException import RPALException
from tokenizer import Token

class Lambda:
    """
    Represents a lambda abstraction in the control structure.
    Stores the index of the control structure (k) and the variables it binds.
    """
    def __init__(self, k, variables):
        self.k = k
        if isinstance(variables, list):
            self.variables = variables
        else:
            self.variables = [variables]
        self.c = None  # Placeholder for the evironment associated with this lambda

    def setC(self, c):
        """
        Sets the environment number associated with this lambda.
        Args:
            c: The environment to associate with this lambda.
        """
        self.c = c
    def getC(self):
        """
        Returns the environment number associated with this lambda.
        """
        return self.c
    
    
    

class Tau:
    """
    Represents a tuple (tau) node in the control structure.
    Stores the number of elements in the tuple.
    """
    def __init__(self, elementNumber):
        self.elementNumber = elementNumber
    
    def getNumberOfElements(self):
        """
        Returns the number of elements in the tuple.
        """
        return self.elementNumber
    
    

class Eta:
    def __init__(self, lambdaNode):
        """
        Represents an eta reduction in the control structure.
        Stores the lambda abstraction associated with this eta.
        Args:
            lambda (Lambda): The lambda abstraction to associate with this eta.
        """
        if not isinstance(lambdaNode, Lambda):
            raise RPALException("Eta reduction must be associated with a Lambda instance")
        self.k = lambdaNode.k
        self.variables = lambdaNode.variables
        self.c = lambdaNode.c

        return
    
    def toLambda(self):
        """
        Generates a Lambda instance from this eta reduction.
        Returns:
            Lambda: The Lambda instance associated with this eta.
        """
        lambdaNode = Lambda(self.k, self.variables)
        lambdaNode.setC(self.c)
        return lambdaNode

class ControlStructure:
    """
    Represents a control structure (delta) which contains a sequence of elements (instructions).
    Each control structure has a unique number (identifier).
    """
    def __init__(self, number):
        self.number = number
        self.elements = []

class CSGenerator:
    """
    Generates control structures (deltas) from an abstract syntax tree (AST).
    Each control structure corresponds to a node or sub-tree in the AST.
    """
    def __init__(self):
        self.controlStructures = []
        
    def getControlStructures(self):
        """
        Returns the list of control structures created.
        Returns:
            list: A list of ControlStructure instances.
        """
        return self.controlStructures
    
    def createControlStructure(self, number, node):
        """
        Creates a new ControlStructure instance with the specified identifier and associates it with the provided AST node.
        Args:
            number (int): The unique identifier for the control structure.
            node (ASTNode): The AST node to associate with this control structure.
        Returns:
            ControlStructure: The newly created ControlStructure instance.
        """
        print(f"Creating control structure with number: {number}")
        cs = ControlStructure(number)
        self.controlStructures.append(cs)
        print("total control structures:", len(self.controlStructures))
        self.addToControlStructure(cs, node)
        return cs  # Return the created control structure for reference

    def addToControlStructure(self, cs, node):
        """
        Recursively adds elements to the given control structure based on the AST node.
        Handles different node types: lambda, ->, tau, and others.
        Args:
            cs (ControlStructure): The control structure to add elements to.
            node (ASTNode): The AST node to process.
        """
        # Handle lambda abstraction nodes
        if node.head == "lambda":
            # If the first child is a comma, it means multiple variables are bound
            if node.child[0].head == ",":
                k = len(self.controlStructures)
                variables = node.child[0].child
                if len(variables) < 1:
                    raise RPALException("Lambda node with ',' must have at least one variable")
                # Create a new control structure for the lambda body
                self.createControlStructure(k, node.child[1])
                variablesToPrint = [var.head.getValue() if isinstance(var.head, Token) else var.head for var in variables]
                print(f"adding<lambda {k}, {variablesToPrint}> to control structure {cs.number}")
                cs.elements.append(Lambda(k, [var.head for var in variables]))
                return

            # Single variable lambda
            if len(node.child) != 2:
                raise RPALException("Lambda node must have exactly two children")
            variable = node.child[0].head
            k = len(self.controlStructures)
            # Create a new control structure for the lambda body
            self.createControlStructure(k, node.child[1])
            printVariable = variable.getValue() if isinstance(variable, Token) else variable
            print(f"adding<lambda {k}, {printVariable}> to control structure {cs.number}")
            cs.elements.append(Lambda(k, variable))
            return
        
        # Handle conditional (if-then-else) nodes
        if node.head == "->":
            if len(node.child) != 3:
                raise RPALException("Node with head '->' must have exactly three children")
            print("creating delta then")
            # Create control structure for 'then' branch
            deltaThen = self.createControlStructure(len(self.controlStructures), node.child[1])
            print("creating delta else")
            # Create control structure for 'else' branch
            deltaElse = self.createControlStructure(len(self.controlStructures), node.child[2])
            print(f"adding< detla(then){deltaThen.number}, delta(else){deltaElse.number}> to control structure {cs.number}")
            cs.elements.append(deltaThen)
            cs.elements.append(deltaElse)
            print(f"adding<beta> to control structure {cs.number}")
            cs.elements.append("beta")

            print(f"calling addToControlStructure for child 0 of node with head '->' {node.child[0].head}")
            # Add the condition to the control structure
            self.addToControlStructure(cs, node.child[0])
            print(f"finished addToControlStructure for child 0 of node with head '->' {node.child[0].head}")
            return
        
        # Handle tuple (tau) nodes
        if node.head == "tau":
            if len(node.child) < 2:
                raise RPALException("Node with head 'tau' must have at least two children")
            print(f"adding<tau({len(node.child)})> to control structure {cs.number}")
            cs.elements.append(Tau(len(node.child)))
            # Add each child of the tuple to the control structure
            for child in node.child:
                print(f"calling addToControlStructure for child {child.head} of node with head 'tau'")
                self.addToControlStructure(cs, child)

            return
        
        # Handle all other nodes (e.g., operators, constants, identifiers)
        label = node.head
        printLabel = label.getValue() if isinstance(label, Token) else label
        print(f"adding<{printLabel}> to control structure {cs.number}")
        cs.elements.append(label)
        # Recursively add children in preorder traversal if they exist
        if node.child and len(node.child) > 0:
            self.addToControlStructure(cs, node.child[0])  
            self.addToControlStructure(cs, node.child[1])

    def generate(self, node):
        """
        Entry point for generating control structures from the ST.
        Args:
            node (Node): The root node of the Standardized Tree.
        Returns:
            list: The list of generated ControlStructure instances.
        """
        if node is None:
            raise RPALException("Node cannot be None")
        self.createControlStructure(0, node)
        return self.getControlStructures()
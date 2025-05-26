from RPALException import RPALException
from tokenizer import Token

class Lambda:
    def __init__(self,k, variable):
        self.k = k
        self.variable = variable

class ControlStructure:
    def __init__(self, number):
        self.number = number
        self.elements = []

class CSGenerator:
    def __init__(self):
        self.controlStructures = []
        
    def getControlStructures(self):
        """
        Returns the list of control structures created.
        Returns:
            list: A list of ControlStructure instances.
        """
        return self.controlStructures
    
    def createControlStructure(self, number,node):
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
        if node.child and len(node.child) > 0:
            self.addToControlStructure(cs, node.child[0])  
            self.addToControlStructure(cs, node.child[1])

        return cs
    
    def addToControlStructure(self, cs, node):
        if node.head == "lambda":
            if len(node.child) != 2:
                raise RPALException("Lambda node must have exactly two children")
            if (type(node.child[0].head) is Token):
                variable = node.child[0].head.getValue()
            elif (type(node.child[0].head) is str):
                variable = node.child[0].head
            k = len(self.controlStructures)
            newCS = self.createControlStructure(k, node.child[1])
            print(f"adding<lambda {k}, {variable}> to control structure {cs.number}")
            cs.elements.append(Lambda(k, variable))
            return
        
        if node.head == "->":
            if len(node.child) != 3:
                raise RPALException("Node with head '->' must have exactly three children")
            print("creating delta then")
            deltaThen = self.createControlStructure(len(self.controlStructures), node.child[1])
            print("creating delta else")
            deltaElse = self.createControlStructure(len(self.controlStructures), node.child[2])
            print(f"adding<-> detla(then){deltaThen.number}, delta(else){deltaElse.number}> to control structure {cs.number}")
            cs.elements.append((deltaThen, deltaElse))
            print(f"adding<beta> to control structure {cs.number}")
            cs.elements.append("beta")

            print(f"calling addToControlStructure for child 0 of node with head '->' {node.child[0].head}")

            self.addToControlStructure(cs, node.child[0])

            return
        if (type(node.head) is Token):
            label = node.head.getValue()
            print(f"adding<{label}> to control structure {cs.number} as node token")
            cs.elements.append(label)
        elif (type(node.head) is str):
            label = node.head
            print(f"adding<{label}> to control structure {cs.number} as node")
            cs.elements.append(label)
            

    def generate(node):
        if node is None:
            raise RPALException("Node cannot be None")
        

        
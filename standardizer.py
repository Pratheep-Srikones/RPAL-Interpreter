from RPALException import RPALException
from parser import Node
from tokenizer import Token
import copy




def checkNodeLabel(node, label):
    """
    Check if the node has the specified label.
    
    Args:
        node: The AST node to check.
        label: The label to look for.
    
    Returns:
        True if the node has the specified label, False otherwise.
    """
    if type(node.head) is Token:
        if node.head.getValue() != label:
            raise RPALException(f"Node has unexpected label: expected {label}, got {node.head.getValue()}")
        
    elif type(node.head) is str:
        if node.head != label:
            raise RPALException(f"Node has unexpected label: expected {label}, got {node.head}")

def checkForChildrenNumber(node, number, forMin=False):
    """
    Check if the node has a child with the specified number.
    
    Args:
        node: The AST node to check.
        number: The number to look for in the children.
    
    Returns:
        True if a child with the specified number exists, False otherwise.
    """
    if forMin:
        if len(node.child) < number:
            raise RPALException(f"Node has fewer children than expected: expected at least {number}, for {node.head} got {len(node.child)}")
    else:
        if len(node.child) != number:
            raise RPALException(f"Node has an unexpected number of children: expected {number}, for {node.head} got {len(node.child)}")

class StandardizeAST:
    """
    Class to standardize the AST by checking node labels and children.
    """
    def __init__(self):
        """
        Initialize the StandardizeAST class.
        """
        pass


    def checkNode(self,node, label, number, forMin=False):
        """
        Check if the node has the specified label and number of children.
        
        Args:
            node: The AST node to check.
            label: The label to look for.
            number: The number of children to check.
            forMin: If True, checks for a minimum number of children.
        
        Raises:
            RPALException: If the node does not match the expected label or number of children.
        """
        #print(f"Checking node: {node.head}, expected label: {label}, expected number of children: {number}, forMin: {forMin}")
        checkNodeLabel(node, label)
        checkForChildrenNumber(node, number, forMin)
        
    def standardizeLet(self,node):
        self.checkNode(node, "let", 2)
        equalNode = node.getChild(0)
        pNode = node.getChild(1)

        self.checkNode(equalNode, "=", 2)
        xNode = equalNode.getChild(0)
        eNode = equalNode.getChild(1)

        node.changeHead("gamma")
        node.clearAllChildren()

        equalNode.changeHead("lambda")
        node.addChild(equalNode)
        node.addChild(eNode)

        equalNode.clearAllChildren()
        equalNode.addChild(xNode)
        equalNode.addChild(pNode)

        return

    def standardizeWhere(self, node):
        self.checkNode(node, "where", 2)
        pNode = node.getChild(0)
        equalNode = node.getChild(1)
        self.checkNode(equalNode, "=", 2)

        xNode = equalNode.getChild(0)
        eNode = equalNode.getChild(1)

        node.changeHead("gamma")
        node.clearAllChildren()
        
        equalNode.changeHead("lambda")
        equalNode.clearAllChildren()
        equalNode.addChild(xNode)
        equalNode.addChild(pNode)
        
        node.addChild(equalNode)
        node.addChild(eNode)

        return
    
    def standardizeFunction(self, node):
        self.checkNode(node, 'fcn_form', 3, forMin=True)

        numberOfVariables = len(node.child) - 2

        pNode = node.getChild(0)
        eNode = node.getChild(numberOfVariables+1)

        vNodes = node.child[1:numberOfVariables+1]

        node.changeHead("=")
        node.clearAllChildren()

        node.addChild(pNode)
        currentNode = node
        for vNode in vNodes:
            lambdaNode = Node("lambda")
            currentNode.addChild(lambdaNode)
            lambdaNode.addChild(vNode)
            currentNode = lambdaNode
        
        currentNode.addChild(eNode)

        return
    
    def standardizeAnd(self, node):
        self.checkNode(node, "and", 2, forMin=True)
        equalNodes = node.child 

        node.changeHead("=")
        node.clearAllChildren()

        tauNode = Node("tau")
        commaNode = Node(",")

        node.addChild(commaNode)
        node.addChild(tauNode)	

        for equalNode in equalNodes:
            self.checkNode(equalNode, "=", 2)
            xNode = equalNode.getChild(0)
            eNode = equalNode.getChild(1)

            commaNode.addChild(xNode)
            tauNode.addChild(eNode) 

        return

    def standardizeWithin(self, node):
        self.checkNode(node, "within", 2)
        leftEqualNode = node.getChild(0)
        rightEqualNode = node.getChild(1)

        self.checkNode(leftEqualNode, "=", 2)
        self.checkNode(rightEqualNode, "=", 2)

        x1Node = leftEqualNode.getChild(0)
        e1Node = leftEqualNode.getChild(1)

        x2Node = rightEqualNode.getChild(0)
        e2Node = rightEqualNode.getChild(1)

        node.changeHead("=")
        node.clearAllChildren()

        gammaNode = Node("gamma")
        lambdaNode = Node("lambda")

        node.addChild(x2Node)
        node.addChild(gammaNode)

        gammaNode.addChild(lambdaNode)
        gammaNode.addChild(e1Node)

        lambdaNode.addChild(x1Node)
        lambdaNode.addChild(e2Node)

        return
    
    def standardizeInfix(self, node):
        self.checkNode(node, '@',3)
        e1Node = node.getChild(0)
        nNode = node.getChild(1)
        e2Node = node.getChild(2)

        node.changeHead("gamma")
        node.clearAllChildren()

        gammaNode = Node("gamma")

        node.addChild(gammaNode)
        node.addChild(e2Node)

        gammaNode.addChild(nNode)
        gammaNode.addChild(e1Node)

        return

    def standardizeRec(self, node):
        self.checkNode(node,"rec", 1)

        equalNode = node.getChild(0)
        self.checkNode(equalNode, "=", 2)
        xNode = equalNode.getChild(0)
        xNodeCopy = copy.deepcopy(xNode)  # Create a copy of xNode
        eNode = equalNode.getChild(1)

        node.changeHead("=")
        node.clearAllChildren()

        gammaNode = Node("gamma")
        lambdaNode = Node("lambda")
        yNode = Node("Y")
        node.addChild(xNode)
        node.addChild(gammaNode)

        gammaNode.addChild(yNode)
        gammaNode.addChild(lambdaNode)

        lambdaNode.addChild(xNodeCopy)
        lambdaNode.addChild(eNode)

        return

    def standardizeMultiParameter(self, node):
        self.checkNode(node, "lambda",3, forMin=True)
        variableCount = len(node.child) - 1
        vNodes = node.child[0:variableCount]

        eNode = node.getChild(variableCount)

        node.clearAllChildren()
        currLambdaNode = node
        for vNode in vNodes:
            currLambdaNode.addChild(vNode)
            lambdaNode = Node("lambda")
            currLambdaNode.addChild(lambdaNode)
            currLambdaNode = lambdaNode
        currLambdaNode.addChild(eNode)



    def standardize(self, node=None):
        if node is None:
            raise RPALException("Node is None")
        if not isinstance(node, Node):
            raise RPALException("Node is not an instance of Node class")
        
        if type(node.head) is str and type(node.head) is not Token:
            #first standardize the childern
            if node.child and len(node.child) > 0:
                for child in node.child:
                    self.standardize(child)

            #then standardize the node itself
            if node.head == "let":
                self.standardizeLet(node)
            elif node.head == "where":
                self.standardizeWhere(node)
            elif node.head == "fcn_form":
                self.standardizeFunction(node)
            elif node.head == "and":
                self.standardizeAnd(node)
            elif node.head == "within":
                self.standardizeWithin(node)
            elif node.head == "@":
                self.standardizeInfix(node)
            elif node.head == "rec":
                self.standardizeRec(node)
            elif node.head == "lambda" and len(node.child) > 1:
                self.standardizeMultiParameter(node)
            
       

    
    


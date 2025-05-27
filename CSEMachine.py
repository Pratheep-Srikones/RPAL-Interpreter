from Environment import Environment
from RPALException import RPALException
from generateCS import ControlStructure, Eta, Lambda, Tau
from tokenizer import Token

# List of supported binary and unary operators
BINARY_OPERATORS = ["+", "-", "*", "/", "eq", "gr", "ge", "ls", "le","aug"]
UNARY_OPERATORS = ["not", "neg"]
BUILTIN_FUNCTIONS = ['print']
OTHER_KEYWORDS = ['nil', 'Y',"Print"]

class CSEMachine:
    """
    The CSEMachine class implements the Control Stack Environment (CSE) machine
    for evaluating RPAL (Right-reference Programming Algorithmic Language) expressions.
    It manages control structures, environments, and a stack to interpret and execute code.
    """

    def __init__(self, controls, environment):
        """
        Initializes the CSEMachine with the given control structures and environment.
        Sets up the control stack and main stack for execution.
        """
        self.controls = controls
        self.controlStack = []
        self.stack = []
        self.currentEnvironment = environment
        self.totalEnvironments = 1

        self.controlStack.append(self.currentEnvironment)
        defaultControl = self.findControlStructure(0)
        if defaultControl is None:
            raise RPALException("Control structure with number 0 not found.")
        if type(defaultControl) is not ControlStructure:
            raise RPALException("Control structure with number 0 is not a valid ControlStructure.")
        if len(defaultControl.elements) == 0:
            raise RPALException("Control structure with number 0 has no elements.")
        if type(defaultControl) is not ControlStructure:
            raise RPALException("Control structure with number 0 is not a valid ControlStructure.")
        self.insertControlStructure(defaultControl)

        self.stack.append(self.currentEnvironment)

    def findControlStructure(self, number):
        """
        Finds and returns the control structure with the specified number.
        Raises an exception if not found.
        """
        for control in self.controls:
            if control.number == number:
                return control
        raise RPALException(f"Control structure with number {number} not found.")
    
    def insertControlStructure(self, control):
        if type(control) is not ControlStructure:
            raise RPALException("Control structure must be an instance of ControlStructure.")
        if len(control.elements) == 0:
            raise RPALException("Control structure must have at least one element.")
        for element in control.elements:
            self.controlStack.append(element)
    

    def rule1(self):
        """
        CSE Rule 1: Handles variable lookup.
        Pops a variable name from the control stack, looks up its value in the current environment,
        and pushes the value onto the stack.
        """
        name = self.controlStack.pop()
        value = self.currentEnvironment.lookUpValue(name)
        self.stack.append(value)
        return

    def rule2(self):
        """
        CSE Rule 2: Handles lambda.
        Pops a Lambda control structure from the control stack, sets its environment,
        and pushes it onto the stack.
        """
        lambdaControl = self.controlStack.pop()
        if (type(lambdaControl) is not Lambda):
            raise RPALException("Expected a Lambda control structure.")
        lambdaControl.setC(self.currentEnvironment.number)
        self.stack.append(lambdaControl)
        return
    
    def rule3(self):
        """No need to implement rule 3 since operator handling is done by rule 6 and 7"""
        pass

    def rule4(self):
        """
        CSE Rule 4: Handles function application (gamma) to lambda.
        Pops 'gamma' from the control stack, applies a Lambda function to a value,
        creates a new environment, and updates the control and main stacks accordingly.
        """
        self.controlStack.pop()
        lambdaControl = self.stack.pop()
        if (type(lambdaControl) is not Lambda):
            raise RPALException("Expected a Lambda control structure.")
        
        variable = lambdaControl.variables[0] if len(lambdaControl.variables) == 1 else lambdaControl.variables
        if type(variable) is Token:
            variable = variable.getValue()
        
        value = self.stack.pop()
        
        if type(value) is Token:
            value = value.getValue()
        #find the control structure for the lambda
        newControl = self.findControlStructure(lambdaControl.k)

        if type(newControl) is not ControlStructure:
            raise RPALException(f"Control structure with number {lambdaControl.k} is not a valid ControlStructure.")
        
        # Create a new environment for the lambda binding with new variable
        newEnv = Environment(self.totalEnvironments, self.currentEnvironment, {variable: value})
        self.currentEnvironment = newEnv
        self.totalEnvironments += 1

        self.controlStack.append(newEnv)
        self.insertControlStructure(newControl)

        self.stack.append(newEnv)
        return
    
    def rule5(self):
        """
        CSE Rule 5: Handles environment removal.
        Pops the environment from the control stack and removes the corresponding environment from the stack.
        """
        self.controlStack.pop()
        self.stack.pop(-2)
        
        # Traverse the control stack to find the first Environment object
        nextEnv = None
        #print("searching for next environment in control stack")
        #print(self.controlStack)
        for i in range(len(self.controlStack)-1, -1, -1):
            #print(f"Checking control stack item at index {i}: {self.controlStack[i]}")
            if type(self.controlStack[i]) is Environment:
                nextEnv = self.controlStack[i]
                break
        self.currentEnvironment = nextEnv
        self.totalEnvironments -= 1

    def rule6(self):
        """
        CSE Rule 6: Handles binary operations.
        Pops an operator from the control stack and two operands from the stack,
        applies the operation, and pushes the result onto the stack.
        """
        operator = self.controlStack.pop()

        operand1 = self.stack.pop()
        operand2 = self.stack.pop()
        if type(operand1) is Token:
            operand1 = operand1.getValue()
        if type(operand2) is Token:
            operand2 = operand2.getValue()
        
        if operator == "+":
            result = operand1 + operand2
        elif operator == "-":
            result = operand1 - operand2
        elif operator == "*":
            result = operand1 * operand2
        elif operator == "/":
            if operand2 == 0:
                raise RPALException("Division by zero.")
            result = int(operand1 / operand2)
        elif operator == "eq":
            result = (operand1 == operand2)
        elif operator == "gr":
            result = (operand1 > operand2)
        elif operator == "ge":
            result = (operand1 >= operand2)
        elif operator == "ls":
            result = (operand1 < operand2)
        elif operator == "le":
            result = (operand1 <= operand2)
        elif operator == "aug":
            if operand1 == "nil":
                result = [operand2]
            elif type(operand1) is list:
                result = operand1 + [operand2]
                

        self.stack.append(result)
        return

    def rule7(self):
        """
        CSE Rule 7: Handles unary operations.
        Pops an operator from the control stack and an operand from the stack,
        applies the operation, and pushes the result onto the stack.
        """
        operator = self.controlStack.pop()
        operand = self.stack.pop()

        if type(operand) is Token:
            operand = operand.getValue()

        if operator == "not":
            result = not operand
        elif operator == "neg":
            result = -operand
        elif operator == "print":
            print(operand)	
        
        self.stack.append(result)
        return
    
    def rule8(self):
        """
        CSE Rule 8: Handles conditional branching (beta).
        Pops 'beta' from the control stack and evaluates the condition from the stack.
        Depending on the condition, inserts the appropriate control structure (delta_then/delta_else branch).
        """
        beta = self.controlStack.pop()
        if beta != "beta":
            raise RPALException("Expected 'beta' in control stack.")
        evaluated = self.stack.pop()
        if evaluated:
            self.controlStack.pop()  # Remove the 'else' branch (not taken)
            deltaThen = self.controlStack.pop()  # Get the 'then' branch control structure
            self.insertControlStructure(deltaThen)
        else:
            deltaElse = self.controlStack.pop()  # Get the 'else' branch control structure
            self.controlStack.pop()  # Remove the 'then' branch (not taken)
            self.insertControlStructure(deltaElse)

    def rule9(self):
        """
        CSE Rule 9: Handles tuple construction (tau).
        Pops a Tau control structure from the control stack and collects the specified number of elements from the stack,
        then pushes the constructed tuple (as a list) onto the stack.
        """
        tau = self.controlStack.pop()
        if type(tau) is not Tau:
            raise RPALException("Expected 'tau' in control stack.")

        numberOfElements = tau.elementNumber
        listOfElements = []
        for i in range(numberOfElements):
            element = self.stack.pop()
            if type(element) is Token:
                element = element.getValue()
            listOfElements.append(element)

        self.stack.append(listOfElements)

    def rule10(self):
        """
        CSE Rule 10: Handles tuple element selection.
        Pops 'gamma' from the control stack, a tuple (list) from the stack, and an index from the stack.
        Pushes the selected tuple element onto the stack (1-based indexing).
        """
        gamma = self.controlStack.pop()
        tupleElements = self.stack.pop()

        if type(gamma) is not str or gamma != "gamma":
            raise RPALException("Expected 'gamma' in control stack.")
        if type(tupleElements) is not list:
            raise RPALException("Expected a list of elements on the stack for 'gamma' operation.")
        index = self.stack.pop()
        if not isinstance(index, int):
            raise RPALException("Index must be an integer.")
        if index < 0 or index >= len(tupleElements):
            raise RPALException("Index out of bounds for tuple elements.")
        #index adjusting RPAL uses 1-based indexing
        result = tupleElements[index-1]
        self.stack.append(result)

    def rule11(self):
        """
        CSE Rule 11: Handles function application (gamma) to a lambda with multiple arguments.
        Pops 'gamma' from the control stack, a Lambda from the stack, and a list of argument values from the stack.
        Binds arguments to lambda variables, creates a new environment, and inserts the lambda's control structure.
        """
        gamma = self.controlStack.pop()
        lambdaControl = self.stack.pop()
        if type(gamma) is not str or gamma != "gamma":
            raise RPALException("Expected 'gamma' in control stack.")
        if type(lambdaControl) is not Lambda:
            raise RPALException("Expected a Lambda control structure on the stack for 'gamma' operation.")
        values = self.stack.pop()
        if type(values) is not list:
            raise RPALException("Expected a list of names on the stack for 'gamma' operation.")
        if len(values) != len(lambdaControl.variables):
            raise RPALException("Number of names does not match number of variables in lambda.")

        dataDict = {}
        for var, name in zip(lambdaControl.variables, values):
            if type(var) is Token:
                var = var.getValue()
            if type(name) is Token:
                name = name.getValue()
            dataDict[var] = name

        # Create a new environment for the lambda application
        newEnv = Environment(self.totalEnvironments, self.currentEnvironment, dataDict)
        self.currentEnvironment = newEnv
        self.totalEnvironments += 1
        self.controlStack.append(newEnv)
        self.stack.append(newEnv)
        newControl = self.findControlStructure(lambdaControl.k)
        if type(newControl) is not ControlStructure:
            raise RPALException(f"Control structure with number {lambdaControl.k} is not a valid ControlStructure.")
        self.insertControlStructure(newControl)

        return

    def rule12(self):
        """
        CSE Rule 12: Handles Y combinator application for recursion.
        Pops 'gamma' from the control stack, 'Y' from the stack, and a Lambda from the stack.
        Wraps the lambda in an Eta structure and pushes it onto the stack.
        """
        gamma = self.controlStack.pop()
        if gamma != "gamma":
            raise RPALException("Expected 'gamma' in control stack.")
        yStar = self.stack.pop()
        if yStar != "Y":
            raise RPALException("Expected 'Y' for yStar in control stack.")
        lambdaControl = self.stack.pop()
        if type(lambdaControl) is not Lambda:
            raise RPALException("Expected a Lambda control structure on the stack for 'gamma' operation.")
        eta  = Eta(lambdaControl)
        self.stack.append(eta)

    def rule13(self):
        """
        CSE Rule 13: Handles Eta structure application (for recursion).
        Converts the Eta on the stack to a Lambda, pushes it back, and adds 'gamma' to the control stack
        to trigger further application.
        """
        eta = self.stack[-1]
        if type(eta) is not Eta:
            raise RPALException("Expected an Eta instance on the stack.")

        newLambda = eta.toLambda()

        self.stack.append(newLambda)
        self.controlStack.append("gamma")

        return
    
    def builtinFunction(self):
        """
        Handles built-in functions.
        Pops a built-in function name from the control stack and applies it to the top of the stack.
        """
        self.controlStack.pop()  # Pop 'gamma'
        functionName = self.stack.pop()
        if functionName not in BUILTIN_FUNCTIONS:
            raise RPALException(f"Unknown built-in function: {functionName}")
        
        value = self.stack[-1]
        if type(value) is Token:
            value = value.getValue()

        if functionName == "print":
            print(value)
            return

        

    def interpret(self):
        """
        Main interpreter loop.
        Processes the control stack and applies the appropriate rules until the control stack is empty.
        Returns the final result of the computation.
        """
        while len(self.controlStack) > 0:
            #NOTE : The rule numbers are similar to the ones in the lecture note.
            if type(self.controlStack[-1]) is Token or self.controlStack[-1] in OTHER_KEYWORDS:
                print("Rule 1")
                self.rule1()
            elif type(self.controlStack[-1]) is Lambda:
                print("Rule 2")
                self.rule2()
            elif self.controlStack[-1] == "gamma" and type(self.stack[-1]) is Lambda and len(self.stack[-1].variables) == 1:
                print("Rule 3")
                self.rule4()
            elif type(self.controlStack[-1]) is Environment:
                print("Rule 5")
                self.rule5()
            elif self.controlStack[-1] in BINARY_OPERATORS:
                print("Rule 6")
                self.rule6()
            elif self.controlStack[-1] in UNARY_OPERATORS:
                print("Rule 7")
                self.rule7()
            elif self.controlStack[-1] == "beta":
                print("Rule 8")
                self.rule8()
            elif type(self.controlStack[-1]) is Tau:
                print("Rule 9")
                self.rule9()
            elif self.controlStack[-1] == "gamma" and type(self.stack[-1]) is list and len(self.stack[-1]) > 0:
                print("Rule 10")
                self.rule10()
            elif self.controlStack[-1] == "gamma" and type(self.stack[-1]) is Lambda and len(self.stack[-1].variables) > 1:
                print("Rule 11")
                self.rule11()
            elif self.controlStack[-1] == "gamma" and type(self.stack[-1]) is str and self.stack[-1] == "Y":
                print("Rule 12")
                self.rule12()
            elif self.controlStack[-1] == "gamma" and type(self.stack[-1]) is Eta:
                print("Rule 13")
                self.rule13()
            elif self.controlStack[-1] == "gamma" and self.stack[-1] in BUILTIN_FUNCTIONS:
                self.builtinFunction()
            else:
                raise RPALException(f"Unknown control structure: {self.controlStack[-1]}")
        
        result = self.stack.pop()
        return result

    
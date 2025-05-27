from Environment import Environment
from RPALException import RPALException
from generateCS import ControlStructure, Lambda, Tau
from tokenizer import Token

# List of supported binary and unary operators
BINARY_OPERATORS = ["+", "-", "*", "/", "eq", "gr", "ge", "ls", "le"]
UNARY_OPERATORS = ["not", "neg"]

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

        # Start with the initial environment on the control stack
        self.controlStack.append(self.currentEnvironment)
        defaultControl = self.findControlStructure(0)
        print(f"[INIT] Initializing CSEMachine with control structure 0: {defaultControl}")
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
        print(f"[INIT] controlStack: {self.controlStack}, stack: {self.stack}")

    def findControlStructure(self, number):
        """
        Finds and returns the control structure with the specified number.
        Raises an exception if not found.
        """
        for control in self.controls:
            if control.number == number:
                print(f"[findCOntrolStructure] Found control structure {number}")
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
        print(f"[rule1] Popped name: {name}")
        value = self.currentEnvironment.lookUpValue(name)
        print(f"[rule1] Looked up value: {value}")
        self.stack.append(value)
        print(f"[rule1] Stack after append: {self.stack}")
        return

    def rule2(self):
        """
        CSE Rule 2: Handles lambda.
        Pops a Lambda control structure from the control stack, sets its environment,
        and pushes it onto the stack.
        """
        lambdaControl = self.controlStack.pop()
        print(f"[rule2] Popped lambdaControl: {lambdaControl}")
        if (type(lambdaControl) is not Lambda):
            raise RPALException("Expected a Lambda control structure.")
        lambdaControl.setC(self.currentEnvironment.number)
        self.stack.append(lambdaControl)
        print(f"[rule2] Stack after append: {self.stack}")
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
        print(f"[rule4] Popped 'gamma' from controlStack")
        lambdaControl = self.stack.pop()
        print(f"[rule4] Popped lambdaControl from stack: {lambdaControl}")
        if (type(lambdaControl) is not Lambda):
            raise RPALException("Expected a Lambda control structure.")
        
        variable = lambdaControl.variables[0] if len(lambdaControl.variables) == 1 else lambdaControl.variables
        if type(variable) is Token:
            variable = variable.getValue()
        
        value = self.stack.pop()
        print(f"[rule4] Popped value from stack: {value}")
        
        if type(value) is Token:
            value = value.getValue()

        newControl = self.findControlStructure(lambdaControl.k)

        if type(newControl) is not ControlStructure:
            raise RPALException(f"Control structure with number {lambdaControl.k} is not a valid ControlStructure.")
        
        newEnv = Environment(self.totalEnvironments, self.currentEnvironment, {variable: value})
        print(f"[rule4] Created new environment: {newEnv}")
        self.currentEnvironment = newEnv
        self.totalEnvironments += 1

        self.controlStack.append(newEnv)
        print(f"[rule4] Appended newEnv to controlStack: {self.controlStack}")
        self.insertControlStructure(newControl)

        print(f"[rule4] controlStack after adding newControl elements: {self.controlStack}")
        self.stack.append(newEnv)
        print(f"[rule4] Stack after append: {self.stack}")
        return
    
    def rule5(self):
        """
        CSE Rule 5: Handles environment removal.
        Pops the environment from the control stack and removes the corresponding environment from the stack.
        """
        popped_env = self.controlStack.pop()
        print(f"[rule5] Popped environment from controlStack: {popped_env}")
        popped_stack_env = self.stack.pop(-2)
        print(f"[rule5] Popped environment from stack: {popped_stack_env}")

    def rule6(self):
        """
        CSE Rule 6: Handles binary operations.
        Pops an operator from the control stack and two operands from the stack,
        applies the operation, and pushes the result onto the stack.
        """
        operator = self.controlStack.pop()
        print(f"[rule6] Popped operator: {operator}")

        operand1 = self.stack.pop()
        operand2 = self.stack.pop()
        print(f"[rule6] Popped operands: {operand1}, {operand2}")
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

        print(f"[rule6] Computed result: {result}")
        self.stack.append(result)
        print(f"[rule6] Stack after append: {self.stack}")
        return

    def rule7(self):
        """
        CSE Rule 7: Handles unary operations.
        Pops an operator from the control stack and an operand from the stack,
        applies the operation, and pushes the result onto the stack.
        """
        operator = self.controlStack.pop()
        print(f"[rule7] Popped operator: {operator}")
        operand = self.stack.pop()
        print(f"[rule7] Popped operand: {operand}")

        if type(operand) is Token:
            operand = operand.getValue()

        if operator == "not":
            result = not operand
        elif operator == "neg":
            result = -operand	
        
        print(f"[rule7] Computed result: {result}")
        self.stack.append(result)
        print(f"[rule7] Stack after append: {self.stack}")
        return
    
    def rule8(self):
        beta = self.controlStack.pop()
        if beta != "beta":
            raise RPALException("Expected 'beta' in control stack.")
        print(f"[rule8] Popped 'beta' from controlStack")
        evaluated = self.stack.pop()
        print(f"[rule8] Popped evaluated expression from stack: {evaluated}")
        if (evaluated):
            print(f"before popping deltaelse: {self.controlStack}")
            self.controlStack.pop()  # Remove the 'else' branch
            print(f"[rule8] Popped 'else' branch from controlStack")
            print(self.controlStack)
            deltaThen = self.controlStack.pop()
            print(type(deltaThen))
            self.insertControlStructure(deltaThen)
        else:
            deltaElse = self.controlStack.pop()
            print(f"[rule8] Popped deltaElse from controlStack: {deltaElse}")
            self.controlStack.pop()  # Remove the 'then' branch
            self.insertControlStructure(deltaElse)

    def rule9(self):
        tau = self.controlStack.pop()
        if type(tau) is not Tau:
            raise RPALException("Expected 'tau' in control stack.")

        numberOfElements = tau.elementNumber
        listOfElements = []
        for i in range(numberOfElements):
            element = self.controlStack.pop()
            print(f"[rule9] Popped element {i}: {element}")
            if type(element) is Token:
                element = element.getValue()
            listOfElements.append(element)
        print(f"[rule9] Collected elements: {listOfElements}")

        self.stack.append(listOfElements)

    def rule10(self):
        gamma = self.controlStack.pop()


    def interpret(self):
        """
        Main interpreter loop.
        Processes the control stack and applies the appropriate rules until the control stack is empty.
        Returns the final result of the computation.
        """
        print("[interpret] Starting interpretation")
        while len(self.controlStack) > 0:
            print(f"[interpret] controlStack: {self.controlStack}")
            print(f"[interpret] stack: {self.stack}")
            if type(self.controlStack[-1]) is Token:
                print("[interpret] Applying rule1")
                self.rule1()
            elif type(self.controlStack[-1]) is Lambda:
                print("[interpret] Applying rule2")
                self.rule2()
            elif self.controlStack[-1] == "gamma" and type(self.stack[0] is Lambda) and len(self.stack[0].variables) == 1:
                print("[interpret] Applying rule4")
                self.rule4()
            elif type(self.controlStack[-1]) is Environment:
                print("[interpret] Applying rule5")
                self.rule5()
            elif self.controlStack[-1] in BINARY_OPERATORS:
                print("[interpret] Applying rule6")
                self.rule6()
            elif self.controlStack[-1] in UNARY_OPERATORS:
                print("[interpret] Applying rule7")
                self.rule7()
            elif self.controlStack[-1] == "beta":
                print("[interpret] Applying rule8")
                self.rule8()
            else:
                raise RPALException(f"Unknown control structure: {self.controlStack[0]}")
        
        result = self.stack.pop()
        print(f"[interpret] Final result: {result}")
        return result

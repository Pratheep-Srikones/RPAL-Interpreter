import sys
from Tokenizer.tokenizer import tokenize
from Parser.parser import Parser
from Parser.standardizer import StandardizeAST
from CSE.generateCS import CSGenerator
from Environment.Environment import Environment
from CSE.CSEMachine import CSEMachine

# Predefined primitive environment variables for the interpreter
PRIMITIVE_ENVIRONMENT_VARIABLES = {
    "Print": "print",
    "nil": "nil",
    "Y": "Y",
    "print": "print",
    "Conc": "conc",
    "Stem": "stem",
    "Stern": "stern",
    "Isinteger": "isInteger",
    "Isstring": "isString",
    "Istruthvalue": "isTruthValue",
    "Isfunction": "isFunction",
    "Istuple": "isTuple",
    "Isdummy": "isDummy",
    "Order": "order",
    "Null": "null",
}

"""
Main entry for the program. Handles command-line args, reads the input file, and tokenizes its contents.

Usage:
    python myrpal.py <file_path>
    python myrpal.py --ast <file_path>

Args:
    <file_path>: Path to input file.
    -ast: (Optional) Print AST.

Behavior:
    - Validates arguments.
    - Reads and prints file lines.
    - Tokenizes lines into a list.
    - Handles errors gracefully.
"""

def main():
    """
    Main function to handle command-line arguments, file reading, tokenization,
    parsing, AST standardization, control structure generation, and interpretation.
    """
    printAST = False

    # Parse command-line arguments
    args = sys.argv[1:]
    if len(args) == 0:
        print("Please provide file path as argument.")
        sys.exit(1)
    if len(args) == 1:
        file_path = args[0]
    elif len(args) == 2:
        if args[0] == "-ast":
            printAST = True
            file_path = args[1]
        else:
            print("Invalid argument. Use -ast to print AST.")
            sys.exit(1)

    # Read the input file and process its contents
    with open(file_path, 'r') as file:
        try:
            lines = file.readlines()
            # Tokenize the input lines
            tokens = tokenize(lines)
            # Parse tokens into an AST
            par = Parser(tokens)
            ast = par.E()

            # Optionally print the AST if requested
            if printAST:
                ast.trav(0)
                print()

            # Standardize the AST for further processing
            StandardizeAST().standardize(ast)
            # Generate control structures from the standardized AST
            csGenerator = CSGenerator()
            controlStructures = csGenerator.generate(ast)

            # Initialize the primitive environment
            primitiveEnvironment = Environment(0, variables=PRIMITIVE_ENVIRONMENT_VARIABLES)
            # Create and run the CSE machine interpreter
            machine = CSEMachine(controlStructures, primitiveEnvironment)
            machine.interpret()

        except Exception as e:
            # Catch and print any errors during processing
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
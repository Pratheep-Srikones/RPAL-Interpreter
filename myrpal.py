import sys
from tokenizer import tokenize
from parser import Parser
from standardizer import StandardizeAST
from generateCS import CSGenerator
from Environment import Environment
from CSEMachine import CSEMachine
"""
Main entry for the program. Handles command-line args, reads the input file, and tokenizes its contents.

Usage:
    python myrpal.py <file_path>
    python myrpal.py --ast <file_path>

Args:
    <file_path>: Path to input file.
    --ast: (Optional) Print AST.

Behavior:
    - Validates arguments.
    - Reads and prints file lines.
    - Tokenizes lines into a list.
    - Handles errors gracefully.
"""
if __name__ == "__main__":
    printAST = False

    args = sys.argv[1:]
    if len(args) == 0:
        print("Please provide file path as argument.")
        sys.exit(1)
    if len(args) ==1:
        file_path = args[0]
    elif len(args) == 2:
        if args[0] == "--ast":
            printAST = True
            file_path = args[1]
        else:
            print("Invalid argument. Use --ast to print AST.")
            sys.exit(1)

    
    with open(file_path, 'r') as file:
        #try:
            lines = file.readlines()
            tokens = tokenize(lines)
            print("Tokens: ")
            for token in tokens:
                print(f'<{token.type}>: <{token.value}>')
            par = Parser(tokens)
            ast = par.E()
            print("*************************************************AST*************************************************")
            
            if printAST:
                ast.trav(0)
            
            print("*************************************************AST*************************************************")
            StandardizeAST().standardize(ast)
            if printAST:
                ast.trav(0)
            else:
                print("AST has been standardized.")

            controlStructures = CSGenerator().generate(ast)

            primitiveEnvironment = Environment(0)
            machine = CSEMachine(controlStructures, primitiveEnvironment)
            output = machine.interpret()
            print("*************************************************Output*************************************************")
            print(output)




        # except Exception as e:
        #     print(f"Error: {e}")
        #     sys.exit(1)

            
import sys
from tokenizer import Token, tokenize
"""
Main entry for the program. Handles command-line args, reads the input file, and tokenizes its contents.

Usage:
    python main.py <file_path>
    python main.py --ast <file_path>

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

    tokens = []
    with open(file_path, 'r') as file:
        try:
            lines = file.readlines()
            tokens = tokenize(lines, tokens)
            # print("Tokens: ")
            # for token in tokens:
            #     print(f'<{token.type}>: <{token.value}>')
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

            
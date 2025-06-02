# Programming Languages Project

## Overview

This project is part of the Semester 4 Programming Languages course. It demonstrates concepts and techniques learned throughout the course, including language syntax, semantics, and implementation.

## Features

- Implementation of core programming language concepts
- Modular and well-documented codebase
- Example programs and usage instructions

## Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Pratheep-Srikones/RPAL-Interpreter.git
    ```
3. **Follow setup instructions** (see below).

## Requirements

- Python

## Usage

1. Execute the RPAL Program
    ```bash
    python myrpal.py filename
    ```
2. Execute the RPAL Program and get the AST
    ```bash
    python myrpal.py -ast filename
    ```

## Project Structure

```
Directory structure:
└── pratheep-srikones-rpal-interpreter/
    ├── readme.md
    ├── myrpal.py #main entry ofthe program
    ├── test #file to write RPAL programs
    ├── CSE/
    │   ├── CSEMachine.py #main interpreter to execute ControlStructure Environment Machine
    │   └── generateCS.py #generateControl Structures based on the Standardized Tree
    ├── Environment/
    │   └── Environment.py #class to represent Execution Environments
    ├── Exception/
    │   └── RPALException.py #wrapper class for Exceptions
    ├── Parser/
    │   ├── parser.py #Parse the tokens and buildthe AST
    │   └── standardizer.py #standardize the AST
    └── Tokenizer/
        └── tokenizer.py #tokenize the input RPAL program from the file

```

## Contributors

- Pratheep Srikones
- Vithurshan Sivanathan


---

*For questions or issues, please contact prathhp231@gmail.com, vithurshansivanathan610@gmail.com*

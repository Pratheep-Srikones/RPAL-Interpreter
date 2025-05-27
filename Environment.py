class Environment:
    def __init__(self, parent=None, variables=None):
        self.parent = parent
        self.variables = variables if variables is not None else {}
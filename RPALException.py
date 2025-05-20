class RPALException(Exception):
    """Base class for all RPAL exceptions."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
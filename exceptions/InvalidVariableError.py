from exceptions.Error import Error


class InvalidVariableError(Error):
    """Exception raised for errors in the input of wrong init file.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message

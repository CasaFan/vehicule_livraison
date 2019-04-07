from exceptions.Error import Error


class InvalidInitFileError(Error):
    """Exception raised for errors in the input of wrong init file.

    Attributes:
        file_path -- the path of file in which the error occurred
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message

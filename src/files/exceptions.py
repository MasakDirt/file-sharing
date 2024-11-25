class BaseFileException(Exception):
    pass


class FileNotFoundInSystemError(BaseFileException):
    def __init__(self, message: str = "File does not exist on the server."):
        self.message = message
        super().__init__(message)

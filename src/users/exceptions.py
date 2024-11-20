class UsersBaseException(Exception):
    pass


class UserNotFoundError(UsersBaseException):
    def __init__(self, message: str = "User not found!") -> None:
        self.message = message
        super().__init__(message)


class UserAlreadyExistsError(UsersBaseException):
    def __init__(
        self, message: str = "User with this credentials already exists!"
    ) -> None:
        self.message = message
        super().__init__(message)


class InvalidPasswordError(UsersBaseException):
    def __init__(self, message: str = "Your passwords are`nt equal") -> None:
        self.message = message
        super().__init__(message)

class MessageException(Exception):
    def __init__(self, message: str = "Invalid error message", *args):
        self.message = message
        super().__init__(self.message, *args)


class NotFoundException(MessageException):
    def __init__(self, message = "Requestet entity not found", *args):
        super().__init__(message, *args)


class NotCreatedException(MessageException):
    def __init__(self, message = "Failed to create entity", *args):
        super().__init__(message, *args)
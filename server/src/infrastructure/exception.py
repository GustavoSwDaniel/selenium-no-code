class BadRequest(Exception):
    pass


class ValidationException(Exception):
    def __init__(self, message: str):
        self.message = message
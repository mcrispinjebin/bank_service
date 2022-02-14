class BadRequest(Exception):
    def __init__(self, message):
        self.message = message
        self.error_code = 400

from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    def __init__(self, status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate credentials", headers = None):
        self.status_code = status_code
        self.detail = detail
        self.headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code, detail, headers)
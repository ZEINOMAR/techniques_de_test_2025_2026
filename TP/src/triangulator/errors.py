"""Shared error utilities."""

def make_error(code: str, message: str):
    return {"code": code, "message": message}

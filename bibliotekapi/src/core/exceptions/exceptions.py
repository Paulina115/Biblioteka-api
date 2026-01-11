"""Module contatining domain exceptions"""

class DomainError(Exception):
    """Base class for all domain errors"""
    pass

class CopyNotFound(DomainError):
    pass

class UserNotFound(DomainError):
    pass

class CopyNotAvailable(DomainError):
    pass

class BookNotBorrowed(DomainError):
    pass
"""Module contatining domain exceptions"""

class DomainError(Exception):
    """Base class for all domain errors"""
    pass

class CopyNotFound(DomainError):
    pass

class UserNotFound(DomainError):
    pass

class BookNotFound(DomainError):
    pass

class CopyNotAvailable(DomainError):
    pass

class BookNotAvailable(DomainError):
    pass

class BookNotBorrowed(DomainError):
    pass

class EmailAlreadyExist(DomainError):
    pass

class BookBorrowed(DomainError):
    pass

class ISBNAlreadyExist(DomainError):
    pass
from dataclasses import dataclass

@dataclass
class Author:
    id: int
    name: str


@dataclass
class Category:
    id: int
    name: str


@dataclass
class Book:
    id: int
    title: str
    author: str
    description: str
    category: Category
    isbn: str
    publication_year: str
    available: bool
    


from __future__ import annotations

import datetime
import os

import httpx
import pydantic


class Books(pydantic.BaseModel):

    books: dict[str, Book]


class Book(pydantic.BaseModel):

    bib_key: str
    details: BookDetails


class BookDetails(pydantic.BaseModel):

    title: str | None = pydantic.Field(default="")
    authors: list[Author] | None = pydantic.Field(default=None)
    publishers: list[str] | None = pydantic.Field(default=None)


class Author(pydantic.BaseModel):

    name: str


def main():
    print("Press ^D to exit when done")
    _ = os.system("stty -echo")
    print(format_header())
    try:
        while True:
            isbn = input()
            book = lookup_isbn(isbn)
            formatted = format_book(isbn, book)
            print(formatted)
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        _ = os.system("stty echo")


def lookup_isbn(isbn: str) -> Book | None:
    resp = httpx.get(
        "http://openlibrary.org/api/books",
        params={
            "bibkeys": f"ISBN:{isbn}",
            "jscmd": "details",
            "format": "json",
        }
    )

    if resp.status_code == 200:
        books = Books(books=resp.json())
        try:
            return next(iter(books.books.values()))
        except StopIteration:
            return None
    else:
        return None


def format_header() -> str:
    return f"| title | authors | publishers | added | isbn\n|---"



def format_book(isbn: str, book: Book | None) -> str:
    if book is None:
        authors = ""
        title = ""
        publishers = ""
    else:
        authors = format_authors(book.details.authors)
        title = book.details.title
        publishers = format_publishers(book.details.publishers)

    today = datetime.date.today().isoformat()

    return f"| {title} | {authors} | {publishers} | {today} | {isbn}"


def format_authors(authors: list[Author] | None) -> str:
    if authors is None:
        return ""
    return ", ".join(author.name for author in authors)


def format_publishers(publishers: list[str] | None) -> str:
    if publishers is None:
        return ""
    return ", ".join(publishers)

import os

import httpx


def lookup_isbn(isbn: str) -> dict:
    resp = httpx.get(
        "http://openlibrary.org/api/books",
        params={
            "bibkeys": f"ISBN:{isbn}",
            "jscmd": "details",
            "format": "json",
        }
    )

    if resp.status_code == 200:
        data: dict = resp.json()
        return next(iter(data.values()))
    else:
        return {}


def format_details(isbn: str, details: dict | None) -> str:
    if details is None:
        authors = ""
        title = ""
        publishers = ""
    else:
        authors = format_authors(details.get("authors"))
        title = details.get("title", "")
        publishers = format_publishers(details.get("publishers"))

    return f"{title} | {authors} | {publishers} | {isbn}"


def format_authors(authors: dict | None) -> str:
    if authors is None:
        return ""
    return ", ".join(author["name"] for author in authors)


def format_publishers(publishers: dict | None) -> str:
    if publishers is None:
        return ""
    return ", ".join(publishers)


def main():
    print("Press ^D to exit when done")
    os.system("stty -echo")
    try:
        while True:
            isbn = input()
            data = lookup_isbn(isbn)
            formatted = format_details(isbn, data.get("details"))
            print(formatted)
    except BaseException:
        pass
    finally:
        os.system("stty echo")

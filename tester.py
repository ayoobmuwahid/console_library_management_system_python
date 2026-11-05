import json
import os
import uuid


class Book:
    def __init__(self, identification, isbn, title, author, category, total_copies, available_copies):
        self.identification = identification
        self.isbn = isbn
        self.title = title
        self.author = author
        self.category = category
        self.total_copies = total_copies
        self.available_copies = available_copies

    def __str__(self):
        return (f"ISBN: {self.isbn} | Title: {self.title} | Author: {self.author} | "
                f"Category: {self.category} | Total Copies: {self.total_copies} | "
                f"Available Copies: {self.available_copies}")

    def to_dict(self):
        return {
            "identification": str(self.identification),  # UUID -> str for JSON
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)  # keys match the __init__ parameter names

    @property
    def total_copies(self):
        return self._total_copies

    @total_copies.setter
    def total_copies(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Total copies must be a non-negative integer.")
        self._total_copies = value

    @property
    def available_copies(self):
        return self._available_copies

    @available_copies.setter
    def available_copies(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Available copies must be a non-negative integer.")
        if value > self._total_copies:
            raise ValueError("Available copies cannot exceed total copies.")
        self._available_copies = value


class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            return  # first run, nothing to load
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.books = [Book.from_dict(d) for d in json.load(f)]
        except (json.JSONDecodeError, TypeError, ValueError, KeyError):
            print("Warning: library file is corrupted, starting with an empty library.")
            self.books = []

    def save(self):
        tmp = self.filename + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=4)
        os.replace(tmp, self.filename)  # write-then-swap avoids a half-written file

    def find_by_isbn(self, isbn):
        return next((b for b in self.books if b.isbn == isbn), None)

    def add_book(self, book):
        if self.find_by_isbn(book.isbn):
            raise ValueError(f"A book with ISBN {book.isbn} already exists.")
        self.books.append(book)
        self.save()

    def del_book(self, book):
        self.books.remove(book)
        self.save()


def is_text(value):
    return value.replace(" ", "").isalpha()


def prompt_for_book(library):
    while True:
        try:
            isbn = int(input("Enter ISBN: "))
            if library.find_by_isbn(isbn):
                print("A book with that ISBN already exists. Try a different one.")
                continue
            title = input("Enter book title: ")
            if not is_text(title):
                raise TypeError("Expected a string")
            author = input("Enter book author: ")
            if not is_text(author):
                raise TypeError("Expected a string")
            category = input("Enter book category: ")
            if not is_text(category):
                raise TypeError("Expected a string")
            total_copies = int(input("Enter total copies: "))
            available_copies = int(input("Enter available copies: "))
            return Book(uuid.uuid4(), isbn, title, author, category, total_copies, available_copies)
        except (ValueError, TypeError):
            print("You have entered invalid input for the above choice")
            continue


def ask_isbn(message):
    """Ask for an ISBN; return an int, or None if the input isn't a number."""
    try:
        return int(input(message))
    except ValueError:
        print("\nInvalid input, try again.\n")
        return None


def main():
    library = Library()
    while True:
        try:
            print(f"{'=' * 35}SELECTION MENU{'=' * 35}")
            user_response = int(input("""
1.) Add a book
2.) View all books
3.) Search for a book
4.) Update book details
5.) Remove a book
6.) Borrow a book
7.) Return a book
8.) Show unavailable books
9.) Filter by category
10.) Show a summary
11.) Exit


Select an option: """))

            if user_response == 11:
                print("Exiting library management system!")
                break
            if user_response > 11 or user_response < 1:
                print("\nPlease select a number between 1 and 11!\n")
                continue
        except ValueError:
            print("\nInvalid input!\n")
            continue

        match user_response:
            case 1:
                book = prompt_for_book(library)
                library.add_book(book)
                print("\nBook added!\n")

            case 2:
                if not library.books:
                    print("\nNo books currently in the library.\n")
                    continue
                width = 155
                print("\n" + " Book List ".center(width, "-"))
                for book in library.books:
                    print(book)
                print("-" * width + "\n")

            case 3:
                reference = input("Enter the title or ISBN of the desired book: ").strip().lower()
                matches = [b for b in library.books
                           if reference == b.title.lower() or reference == str(b.isbn)]
                if matches:
                    print()
                    for book in matches:
                        print(book)
                    print()
                else:
                    print("\nNo book found with that title or ISBN.\n")

            case 4:
                if not library.books:
                    print("\nNo books currently in the library.\n")
                    continue
                book_isbn = ask_isbn("Enter the book ISBN: ")
                if book_isbn is None:
                    continue
                book = library.find_by_isbn(book_isbn)
                if book is None:
                    print("\nNo book found with that ISBN.\n")
                    continue

                print(f"Current details of book: {book}")
                print("Press Enter to keep the current value.\n")

                new_title = input(f"Title [{book.title}]: ")
                if new_title != "":
                    book.title = new_title

                new_author = input(f"Author [{book.author}]: ")
                if new_author != "":
                    book.author = new_author

                new_category = input(f"Category [{book.category}]: ")
                if new_category != "":
                    book.category = new_category

                new_total = input(f"Total copies [{book.total_copies}]: ")
                if new_total != "":
                    if new_total.isdigit():
                        book.total_copies = int(new_total)
                    else:
                        print("Invalid number, total copies not changed.")

                new_available = input(f"Available copies [{book.available_copies}]: ")
                if new_available != "":
                    if new_available.isdigit():
                        try:
                            book.available_copies = int(new_available)
                        except ValueError as e:
                            print(f"{e} Available copies not changed.")
                    else:
                        print("Invalid number, available copies not changed.")

                if book.available_copies > book.total_copies:
                    book.available_copies = book.total_copies
                    print("\nAvailable copies cannot exceed total copies, "
                          "so available is now equal to total copies.")

                library.save()
                print("\nBook updated!\n")

            case 5:
                if not library.books:
                    print("\nNo books currently in the library.\n")
                    continue
                book_isbn = ask_isbn("Enter the book ISBN: ")
                if book_isbn is None:
                    continue
                book = library.find_by_isbn(book_isbn)
                if book is None:
                    print("\nNo book found with that ISBN.\n")
                    continue
                library.del_book(book)
                print("\nBook deleted!\n")

            case 6:
                if not library.books:
                    print("\nNo books currently in the library.\n")
                    continue
                book_isbn = ask_isbn("Enter the ISBN of the book you would like to borrow: ")
                if book_isbn is None:
                    continue
                book = library.find_by_isbn(book_isbn)
                if book is None:
                    print("\nNo book found with that ISBN.\n")
                elif book.available_copies == 0:
                    print("\nSorry, no copies of that book are currently available.\n")
                else:
                    book.available_copies -= 1
                    library.save()
                    print("\nBook borrowed successfully!\n")

            case 7:
                if not library.books:
                    print("\nNo books currently in the library.\n")
                    continue
                book_isbn = ask_isbn("Enter the ISBN of the book you would like to return: ")
                if book_isbn is None:
                    continue
                book = library.find_by_isbn(book_isbn)
                if book is None:
                    print("\nNo book found with that ISBN.\n")
                elif book.available_copies >= book.total_copies:
                    print("\nAll copies of that book are already in the library.\n")
                else:
                    book.available_copies += 1
                    library.save()
                    print("\nBook successfully returned!\n")

            case 8:
                if not library.books:
                    print("\nNo books currently in the library.\n")
                    continue
                unavailable = [b for b in library.books if b.available_copies == 0]
                if not unavailable:
                    print("\nAll books are currently available.\n")
                    continue
                print("\nThe books below are currently unavailable:")
                for book in unavailable:
                    print(f"ISBN: {book.isbn} | Title: {book.title}")
                print()

            case 9:
                if not library.books:
                    print("\nNo books currently in the library.\n")
                    continue
                category = input("Enter the category to filter by: ").strip().lower()
                matches = [b for b in library.books if b.category.lower() == category]
                if matches:
                    print()
                    for book in matches:
                        print(book)
                    print()
                else:
                    print("\nNo books found in that category.\n")

            case 10:
                if not library.books:
                    print("\nNo books currently in the library.\n")
                    continue
                sum_total = sum(b.total_copies for b in library.books)
                sum_available = sum(b.available_copies for b in library.books)

                print(f"\n{'=' * 35} SUMMARY {'=' * 35}")
                print(f"Titles: {len(library.books)}")
                print(f"Total copies: {sum_total}")
                print(f"Available copies: {sum_available}")
                print(f"{'=' * 79}\n")


if __name__ == "__main__":
    main()
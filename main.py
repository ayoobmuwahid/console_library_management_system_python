import csv
import os
import uuid

FIELDS = ["identification", "isbn", "title", "author",
          "category", "total_copies", "available_copies"]


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
        return str({"identification": self.identification,
                    "isbn": self.isbn,
                    "title": self.title,
                    "author": self.author,
                    "category": self.category,
                    "total_copies": self.total_copies,
                    "available_copies": self.available_copies})

    def to_row(self):
        return [self.identification, self.isbn, self.title, self.author,
                self.category, self.total_copies, self.available_copies]

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
    def __init__(self, filename="books.csv"):
        self.filename = filename

    def get_books(self):
        if not os.path.exists(self.filename):
            return []
        books = []
        with open(self.filename, newline="") as file:
            for row in csv.DictReader(file):
                books.append(Book(row["identification"],
                                  int(row["isbn"]),
                                  row["title"],
                                  row["author"],
                                  row["category"],
                                  int(row["total_copies"]),
                                  int(row["available_copies"])))
        return books

    def save_books(self, books):
        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(FIELDS)
            for book in books:
                writer.writerow(book.to_row())

    def add_book(self, book):
        is_new = not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0
        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)
            if is_new:
                writer.writerow(FIELDS)
            writer.writerow(book.to_row())


def prompt_for_book(existing_isbns):
    while True:
        try:
            isbn = int(input("Enter ISBN: "))
            if isbn in existing_isbns:
                print("\nError: A book with this ISBN already exists! Please try a different ISBN.\n")
                continue

            title = input("Enter book title: ")
            if not title.replace(" ", "").isalpha():
                raise TypeError("Expected a string")

            author = input("Enter book author: ")
            if not author.replace(" ", "").isalpha():
                raise TypeError("Expected a string")

            categories = [
                "Fiction", "Nonfiction", "Science Fiction", "Fantasy",
                "Mystery", "Biography", "History", "Science",
                "Romance", "Self Help"
            ]

            while True:
                try:
                    print("\nCATEGORIES:\n")
                    print("""
                    1) Fiction
                    2) Nonfiction
                    3) Science Fiction
                    4) Fantasy
                    5) Mystery
                    6) Biography
                    7) History
                    8) Science
                    9) Romance
                    10) Self Help\n""")

                    cat_choice = int(input("Choose a category: "))

                    if 1 <= cat_choice <= 10:
                        category = categories[cat_choice - 1]
                        break
                    else:
                        print("\nPlease select a number between 1 and 10!\n")
                except ValueError:
                    print("\nInvalid input! Please enter a number.\n")
            total_copies = int(input("Enter total copies: "))
            available_copies = int(input("Enter available copies: "))
            identification = uuid.uuid4()
            return Book(str(identification), isbn, title, author, category, total_copies, available_copies)

        except (ValueError, TypeError):
            print("You have entered invalid input for the above choice\n")
            continue

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
            if user_response > 10 or user_response < 1:
                print("\nPlease select a number between 1 and 11!\n")
                continue
        except ValueError:
            print("\nInvalid input!\n")
            continue

        match user_response:
            case 1:
                existing_books = library.get_books()
                existing_isbns = {b.isbn for b in existing_books}
                book = prompt_for_book(existing_isbns)
                library.add_book(book)
                print("\nBook added!\n")
                continue

            case 2:
                books = library.get_books()
                if not books:
                    print("\nNo books currently in the library.\n")
                else:
                    width = 155
                    print("\n" + " Book List ".center(width, "-"))
                    for book in books:
                        print(
                            f"ISBN: {book.isbn} | Title: {book.title} | Author: {book.author} | "
                            f"Category: {book.category} | Total Copies: {book.total_copies} | "
                            f"Available Copies: {book.available_copies}")
                    print("-" * width + "\n")
                continue

            case 3:
                books = library.get_books()
                reference = input("Enter the title or ISBN of the desired book: ").lower()
                book_found = False

                for book in books:
                    if reference == book.title.lower() or reference == str(book.isbn):
                        print(f"ISBN: {book.isbn} | Title: {book.title} | Author: {book.author} | "
                              f"Category: {book.category} | Total Copies: {book.total_copies} | "
                              f"Available Copies: {book.available_copies}")
                        book_found = True
                        break

                if not book_found:
                    print("\nNo book found with that title or ISBN.\n")
                continue

            case 4:
                books = library.get_books()
                try:
                    if not books:
                        print("\nNo books currently in the library.\n")
                        continue
                    book_isbn = int(input("Enter the book ISBN: "))

                    book_found = False
                    for book in books:
                        if book.isbn == book_isbn:
                            book_found = True
                            print(f"Current details of books: {book}")
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
                                    book.available_copies = int(new_available)
                                else:
                                    print("Invalid number, available copies not changed.")

                            if book.available_copies > book.total_copies:
                                book.available_copies = book.total_copies
                                print("\nAvailable copies cannot exceed total copies, "
                                      "so available is now equal to total copies.\n")

                            library.save_books(books)
                            print("\nBook updated!\n")
                            break
                except ValueError:
                    print("\nInvalid input, try again.\n")
                    continue

                if not book_found:
                    print("\nNo book found with that ISBN.\n")
                continue

            case 5:
                books = library.get_books()
                try:
                    if not books:
                        print("\nNo books currently in the library.\n")
                        continue
                    book_isbn = int(input("Enter the book ISBN: "))

                    book_found = False
                    for book in books:
                        if book.isbn == book_isbn:
                            book_found = True
                            books.remove(book)
                            library.save_books(books)
                            print("\nBook deleted!\n")
                            break

                    if not book_found:
                        print("\nNo book found with that ISBN.\n")
                    continue
                except ValueError:
                    print("\nInvalid input, try again.\n")
                    continue

            case 6:
                books = library.get_books()
                try:
                    if not books:
                        print("\nNo books currently in the library.\n")
                        continue
                    book_isbn = int(input("Enter the ISBN of the book you would like to borrow: "))

                    book_found = False
                    for book in books:
                        if book.isbn == book_isbn:
                            book_found = True
                            if book.available_copies == 0:
                                print("\nNo copies of that book are currently available.\n")
                            else:
                                book.available_copies -= 1
                                library.save_books(books)
                                print("\nBook borrowed successfully!\n")
                            break

                    if not book_found:
                        print("\nNo book found with that ISBN.\n")
                    continue
                except ValueError:
                    print("\nInvalid input, try again.\n")
                    continue

            case 7:
                books = library.get_books()
                try:
                    if not books:
                        print("\nNo books currently in the library.\n")
                        continue
                    book_isbn = int(input("Enter the ISBN of the book you would like to return: "))

                    book_found = False
                    for book in books:
                        if book.isbn == book_isbn:
                            book_found = True
                            if book.available_copies == book.total_copies:
                                print("\nAll copies of that book are already in the library.\n")
                            else:
                                book.available_copies += 1
                                library.save_books(books)
                                print("\nBook successfully returned!\n")
                            break

                    if not book_found:
                        print("\nNo book found with that ISBN.\n")
                    continue
                except ValueError:
                    print("\nInvalid input, try again.\n")
                    continue

            case 8:
                books = library.get_books()
                if not books:
                    print("\nNo books currently in the library.\n")
                    continue

                unavailable = [b for b in books if b.available_copies == 0]
                if unavailable:
                    print("\nThe books below are currently unavailable.\n")
                    for book in unavailable:
                        print(f"ISBN: {book.isbn} | Title: {book.title}")
                    print()
                else:
                    print("\nAll books are currently available.\n")
                continue

            case 9:
                books = library.get_books()
                if not books:
                    print("\nNo books currently in the library.\n")
                    continue

            case 10:
                books = library.get_books()
                if not books:
                    print("\nNo books currently in the library.\n")
                    continue

                sum_total = 0
                sum_available = 0

                for book in books:
                    sum_total += book.total_copies
                    sum_available += book.available_copies

                print(f"\n{'=' * 35} SUMMARY {'=' * 35}")
                print(f"Titles: {len(books)}")
                print(f"Total copies: {sum_total}")
                print(f"Available copies: {sum_available}")
                print(f"{'=' * 79}\n")
                continue


main()

class Book:
    def __init__(self, identity, title, author, category, total_copies, available_copies):
        self.identity = identity
        self.title = title
        self.author = author
        self.category = category
        self.total_copies = total_copies
        self.available_copies = available_copies

    def __str__(self):
        return str({"identity": self.identity,
                    "title": self.title,
                    "author": self.author,
                    "category": self.category,
                    "total_copies": self.total_copies,
                    "available_copies": self.available_copies})

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)


def prompt_for_book():
    while True:
        try:
            identity = int(input("Enter identity: "))
            title = input("Enter book title: ")
            if not title.replace(" ", "").isalpha():
                raise TypeError("Expected a string")
            author = input("Enter book author: ")
            if not author.replace(" ", "").isalpha():
                raise TypeError("Expected a string")
            category = input("Enter book category: ")
            if not category.replace(" ", "").isalpha():
                raise TypeError("Expected a string")
            total_copies = int(input("Enter total copies: "))
            available_copies = int(input("Enter available copies: "))
            if available_copies > total_copies:
                print("Available copies exceeds total copies.")
                continue
        except (ValueError, TypeError):
            print("You have entered invalid input for the above choice")
            continue
        else:
            return Book(identity, title, author, category, total_copies, available_copies)



def main():
    library = Library()
    while True:
        try:
            print("===================================SELECTION MENU===================================")
            user_response = int(input("""
1.) Add a book
2.) View all books
3.) Search for a book
4.) Update book details
5.) Remove a book
6.) Borrow a book
7.) Return a book
8.) Filter by category
9.) Show unavailable books
10.) Show a summary
            
Select an option: """))

            if user_response == 0:
                print(f"Exiting library management system!")
                break
            if user_response > 10 or user_response < 1:
                print("\nPlease select a number between 1 and 10!\n")
                continue
        except ValueError:
            print("\nInvalid input!\n")
            continue

        match user_response:
            case 1:
                book = prompt_for_book()
                library.add_book(book)
                print("\nBook added!\n")
                continue
            case 2:
                if not library.books:
                    print("\nNo books currently in the library.\n")
                else:
                    print(
                        "\n------------------------------------------------------------------------ Book List ------------------------------------------------------------------------")
                    for book in library.books:
                        print(
                            f"ID: {book.identity} | Title: {book.title} | Author: {book.author} | Category: {book.category} | Total Copies: {book.total_copies} | Available Copies: {book.available_copies}")
                    print(
                        "-----------------------------------------------------------------------------------------------------------------------------------------------------------\n")
                    continue

            case 3:
                    reference = input("Enter the title or ID of the desired book: ").lower()
                    book_found = False

                    for book in library.books:
                        if reference == book.title.lower() or reference == str(book.identity):
                            print(f"ID: {book.identity} | Title: {book.title} | Author: {book.author} | "
                                  f"Category: {book.category} | Total Copies: {book.total_copies} | "
                                  f"Available Copies: {book.available_copies}")
                            book_found = True

                    if not book_found:
                        print("\nNo book found with that title.\n")
                    continue

            case 4:
                if not library.books:
                    print("\nNo books currently in the library.\n")
                    continue
                book_id = input("Enter the book ID: ")
                book_id = int(book_id)

                book_found = False
                for book in library.books:
                    if book.identity == book_id:
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
                            print("\nAvailable copies cannot exceed total copies therefore available is now equal to toal copies.\n")

                        print("\nBook updated!\n")
                        break

                    if not book_found:
                        print("\nNo book found with that ID.\n")
                    continue


main()
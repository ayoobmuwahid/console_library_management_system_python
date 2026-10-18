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


def add_book():
    while True:
        try:
            identity = input("Enter identity: ")
            if isinstance(identity, (int, float, bool)):
                raise TypeError("Expected a string")
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
    books = []
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
                book = add_book()
                books.append(book)
                print("\nBook added!\n")
                continue
            case 2:
                if not books:
                    print("\nNo books currently in the library.\n")
                else:
                    print(
                        "\n------------------------------------------------------------------------ Book List ------------------------------------------------------------------------")
                    for book in books:
                        print(
                            f"ID: {book.identity} | Title: {book.title} | Author: {book.author} | Category: {book.category} | Total Copies: {book.total_copies} | Available Copies: {book.available_copies}")
                    print(
                        "-----------------------------------------------------------------------------------------------------------------------------------------------------------\n")
                    continue


main()

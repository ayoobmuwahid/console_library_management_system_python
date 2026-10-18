

def add_book():
    while True:
        try:

            identity = input("Enter identity: ")
            if not identity.replace(" ", "").isalnum():
                raise TypeError("Expected a string")
            name = input("Enter book title: ")
            if not name.replace(" ", "").isalnum():
                raise TypeError("Expected a string")
            author = input("Enter book author: ")
            if not author.replace(" ", "").isalnum():
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
            print(identity, name, author, category, total_copies, available_copies)



add_book()
xxx
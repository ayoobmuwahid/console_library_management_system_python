import sys


def main():
    while True:
        try:

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
            if 1 <= user_response <= 10:
                print(f"You selected option {user_response}")
                break
            elif user_response == 0:
                print(f"Exiting library management system!")
                break
            elif user_response > 10 or user_response < 1:
                print("\nPlease select a number between 1 and 10!\n")
        except ValueError:
            print("\nInvalid input!\n")

main()

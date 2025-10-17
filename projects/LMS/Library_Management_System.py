# Importing regular expression to check for patterns in strings.
import re

# Creating the book class
class Book:
    def __init__(self,title,author,isbn):
        # Creating the title, author, isbn, and availability status for each book
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True # Default for when a new book is available
        
    def toggle_availibility(self):
        # Adding the ability to switch whether a book is available or not
        self.is_available = not self.is_available
        
# Creating the member class
class Member:
    def __init__(self,name,email):
        # Validating the user email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError ("Invalid format for email!") # Error message of wrong email format is used
        self.name = name
        self.email = email.lower() # Storing emails in lower case for format consistency
        self.books_borrowed = [] # List of the ISBN numbers which the member has borrowed
    
    # Creating the function to borrow book and store the isbn in a list    
    def borrow_book(self, isbn):
        # Adding the book ISBN number to the books borrowed list
        if isbn not in self.books_borrowed:
            self.books_borrowed.append(isbn)
            
    # Creating the function to return the book and remove ISBN from the list
    def return_book(self,isbn):
        # Removing the book ISBN number from the books borrowed list
        if isbn in self.books_borrowed:
            self.books_borrowed.remove(isbn)
            
# Creating the library class
class Library:
    def __init__(self):
        # Storing the books in a dictionary where the ISBN is key and the book object is the value
        self.books = {}
        # Storing the members in a dictionary where email is key and memeber object is the value
        self.members = {}
    
    # Adding a new book to the library
    def add_book(self,title,author,isbn):
        if isbn in self.books:
            print ("A book with this ISBN already exists.")
            return
        self.books[isbn] = Book (title, author, isbn)
        print(f"Book {title} added successsfully.")
        
    # Registering a new member to the library
    def register_member(self,name,email):
        if email in self.members:
            print("Already a registered member.")
            return
        try:
            self.members[email] = Member(name,email)
            print(f"Member {name} registered successfully.")
        except ValueError as e: #cathing an invalid email error
            print("Error: ", e)
    
    # Creating the function to search books by title or author
    def search_books(self, query):
        results = []
        for book in self.books.values():
            if query.lower() in book.title.lower() or query.lower() in book.author.lower():
                results.append(book)
        return results
    # Checking out a book by the ISBN number
    def checkout_book(self,isbn,email):
        email = email.lower()
        if isbn not in self.books:
            print("Book is not found.")
            return
        if email not in self.members:
            print("Member not found.")
            return
        
        book = self.books[isbn]
        member = self.members[email]
        
        if not book.is_available:
            print("Book is not available for checkout. ")
            return
        
        # Marking the book as checked out
        book.toggle_availibility()
        member.borrow_book(isbn)
        print(f"Book, {book.title} checked out to member, {member.name}.")
    
    # Creating function to return a book
    def return_book(self,isbn,email):
        email = email.lower()
        if isbn not in self.books:
            print("Book not found. ")
            return
        if email not in self.members:
            print("Member not found. ")
            return
        
        book = self.books[isbn]
        member = self.members[email]
        
        if isbn not in member.books_borrowed:
            print(f"{member.name} did not borrow this book. ")
            return
        
        # Marking the book as available again
        book.toggle_availibility()
        member.return_book(isbn)
        print(f"Book, {book.title} returned by member, {member.name}")               
                
    # Creating the function to list all the books
    def list_books(self):
        if not self.books:
            print("No books in the library.")
            return
        for b in self.books.values():
            status = "Available" if b.is_available else "Checked out"
            print(f"{b.isbn} - {b.title} by {b.author}: [{status}]")
            
    # Creating the function to list all the members
    def list_members(self):
        if not self.members:
            print("No members registered.")
            return
        for m in self.members.values():
            borrowed = ",".join(m.books_borrowed) if m.books_borrowed else "None"
            print(f"{m.name} - {m.email} Borrowed: {borrowed}.")

# Creating the menu function
def menu():
    # Creating the library object
    library = Library()
    
    while True:
        # Displaying the options
        print('\n--- Library Menu ---')
        print('1. Add Book')
        print('2. List Books')
        print('3. Search Books')
        print('4. Register Member')
        print('5. List Members')
        print('6. Checkout Book')
        print('7. Return Book')
        print('0. Exit')
        
        # Getting the user choice
        choice = input ("Enter choice: ")
        
        # Navigation the menu based on the user choice
        if choice == "1":
            title = input("Enter the book title: ")
            author = input("Enter the author of the book: ")
            isbn = input("Enter ISBN: ")
            library.add_book(title,author,isbn)
        
        elif choice == "2":
            library.list_books()
        
        elif choice == "3":
            query = input("Search book by author or title: ")
            results = library.search_books(query)
            if results:
                for b in results:
                    print(f"{b.isbn} - {b.title} by {b.author}")
            else:
                print("No books found. ")
        
        elif choice == "4":
            name = input("Enter name: ")
            email = input("Enter email: ")
            library.register_member(name, email)
        
        elif choice == "5":
            library.list_members()
            
        elif choice == "6":
            isbn = input("Enter ISBN number to checkout: ")
            email = input("Enter member email: ")
            library.checkout_book(isbn, email)
            
        elif choice == "7":
            isbn = input("Enter ISBN number to return: ")
            email = input("Enter member email: ")
            library.return_book(isbn, email)
        
        elif choice == "0":
            print("Goodbye!")
            break
        
        # Wrong user choice handling
        else:
            print("Invalid choice, try again")
            
# Running the program
if __name__ == "__main__":
    menu()
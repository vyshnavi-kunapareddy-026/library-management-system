from book_utils import *

def greet_user():
    """
    Greets the user and provides instructions.
    """
    print("Welcome to the Book Recommendation System!")
    print("You can search for books by title, author, or genre.")
    print("You can also get recommendations based on books you liked.")
    print("Type 'exit' to quit the program.")
    username_input = input("Please enter your name: ")
    print(f"Hello, {username_input}! Let's find some great books for you.")
    print(f"Let me look you up in the database, {username_input}...")
    load_dotenv()
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    conn = get_connection(db_host, db_port, db_name, db_user, db_password)
    if conn is None:
        print("Failed to connect to the database.")
        return
    user_exists= check_user_exists(username_input, conn)
    if user_exists:
        print(f"Welcome back, {username_input}!")
        print(f"Here are some options for you:")
        print(f"1. Search for books")
        print(f"2. Get book recommendations based on your previous checouts")
        print(f"3. Get book recommendations based on a book you liked")
        print(f"4.View your borrwed log")
        print(f"5. Borrow a book")
        print("6. Exit")
        user_choice = input("Please choose an option (1-5): ").strip()
        if user_choice == "1":
            search_books()
        elif user_choice == "2":
            print("Getting recommendations based on your previous checkouts...")
            book_details = get_user_book_details(username_input, conn)
            if book_details.empty:
                print("No previous checkouts found. Please borrow some books first.")
                user_choice = input("Would you like to borrow a book? (yes/no): ").strip().lower()
                if user_choice == "yes":
                    book_name = input("Please enter the name of the book you want to borrow: ").strip()
                    borrow= borrow_book(book_name, username_input, conn)
                    if borrow:
                        print(f"You have successfully borrowed '{book_name}'.")
        elif user_choice == "3":
            print("Getting recommendations based on a book you liked...")



            # Here you would typically call a function to get recommendations based on previous checkouts
    else:
        print(f"Hello, {username_input}! It seems like you're new here. Let's get you started.")
        print(f"You can choose to be a member if you want me to remember your preferences.")
        print(f"Or you can just search for books, get recommendations without being a member.")
        member_choice = input("Would you like to become a member? (yes/no): ").strip().lower()
        if member_choice == "yes":
            print(f"Great! Let's get you signed up, {username_input}.")
            email= input("Please enter your email address: ").strip()
            if not email:
                print("Email is required to create a member account.")
                return
            user_Details={'username': username_input, 'email': email}
            createUser=create_user(user_Details, conn)
            if createUser:
                print(f"Welcome to the Book Recommendation System, {username_input}! You can now search for books and get personalized recommendations.")
            else:
                print("There was an issue creating your account. Please try again later.")
            print(f"Here are some options for you:")
            print(f"1. Search for books")
            print(f"2. Get book recommendations based on a book you liked")
            print(f"3.Exit")




            # Here you would typically collect more user details and insert them into the database

if __name__ == "__main__":
    greet_user()

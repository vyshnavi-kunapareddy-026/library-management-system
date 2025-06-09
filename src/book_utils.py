from db_connection import get_connection
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import pandas as pd
import random
import spacy

def get_all_books():
    try:
        # use os.getenv to get DB credentials (no need to call load_dotenv here now)
        conn = get_connection(
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME"),
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
        )
        if conn is None:
            return [], "Failed to connect to the database."

        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM books")
            results = cursor.fetchall()
            books_list = results  # Since cursor returns dicts with RealDictCursor
        return books_list, None
    except Exception as e:
        return [], str(e)



def search_books():
    """
    Searches for books in the database based on user input.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Get database connection details from environment variables
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    # Establish a connection to the database
    conn = get_connection(db_host, db_port, db_name, db_user, db_password)

    if conn is None:
        print("Failed to connect to the database.")
        return

    # Get user input for search criteria
    search_criteria = input("Enter search criteria (title, author, genre): ").strip().lower()

    # Define the SQL query based on user input
    query = sql.SQL("SELECT * FROM books WHERE title ILIKE %s OR author ILIKE %s OR genre ILIKE %s")

    # Execute the query and fetch results
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (f"%{search_criteria}%", f"%{search_criteria}%", f"%{search_criteria}%"))
            results = cursor.fetchall()

            # Check if any results were found
            if results:
                # Convert results to a DataFrame for better readability
                df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
                print(df)
            else:
                print("No books found matching the criteria.")

    except Exception as e:
        print("Error executing query:", e)

    finally:
        # Close the database connection
        conn.close()
        print("Connection closed.")

def extract_references_from_db(user_input, conn):
    """Try to match parts of user input to known book titles or authors"""
    print(f"User input: {user_input}")
    cur = conn.cursor()

    # Match input to book titles
    cur.execute("SELECT title, author, genre FROM Books")
    all_books = cur.fetchall()

    for title, author, genre in all_books:
        # print(f"Checking against title: {title}, author: {author}, genre: {genre}")
        if title.lower() in user_input.lower():
            return title, author, genre
        if author.lower() in user_input.lower():
            return None, author, genre

    return None, None, None

def recommend_similar_books(title, author, genre, conn):
    cur = conn.cursor()

    if title and author:
        print(f"\nYou liked **{title}** by {author}.\nHere are more books by the same author:")
        cur.execute("SELECT title FROM Books WHERE author = %s AND title != %s", (author, title))
        recs = cur.fetchall()
        if not recs:
            print("No other books found by this author.")
        else:
            for row in random.sample(recs, min(5, len(recs))):
                print(f"- {row[0]}")

    elif author:
        print(f"\nYou mentioned {author}. Here are more books by them:")
        cur.execute("SELECT title FROM Books WHERE author = %s", (author,))
        recs = cur.fetchall()
        for row in random.sample(recs, min(5, len(recs))):
            print(f"- {row[0]}")

    elif genre:
        print(f"\nRecommending some books in the '{genre}' genre:")
        cur.execute("SELECT title, author FROM Books WHERE genre = %s", (genre,))
        recs = cur.fetchall()
        for row in random.sample(recs, min(5, len(recs))):
            print(f"- {row[0]} by {row[1]}")
    else:
        print("Sorry, I couldn't find a reference in your message.")

    cur.close()


def recommend_by_natural_input_old():


    load_dotenv()

    # Get database connection details from environment variables
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    # print(f"Connecting to the database at {db_host}:{db_port} type {type(db_host)} {type(db_port)}...")

    # DB connection
    conn = get_connection(db_host, db_port, db_name, db_user, db_password)
    if conn is None:
        print("Failed to connect to the database.")
        return
    user_input = input("Tell me about a book you liked: ")
    title, author, genre = extract_references_from_db(user_input, conn)
    recommend_similar_books(title, author, genre, conn)

    conn.close()

def recommend_by_natural_input():
    """
    Recommends books based on natural language input from the user.
    """
    load_dotenv()

    # Get database connection details from environment variables
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    # DB connection
    conn = get_connection(db_host, db_port, db_name, db_user, db_password)
    if conn is None:
        print("Failed to connect to the database.")
        return

    nlp = spacy.load("en_core_web_sm")

    user_input = input("Tell me about a book you liked: ")
    doc = nlp(user_input)

    title, author, genre = None, None, None

    for ent in doc.ents:
        if ent.label_ == "WORK_OF_ART":
            title = ent.text
        elif ent.label_ == "PERSON":
            author = ent.text
        elif ent.label_ == "GPE":  # Assuming GPE might represent genre in some contexts
            genre = ent.text

    recommend_similar_books(title, author, genre, conn)

    conn.close()

def check_user_exists(username, conn):
    """
    Checks if a user exists in the database.
    """
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM members WHERE name = %s", (username,))
    exists = cur.fetchone()[0] > 0
    cur.close()
    return exists

def get_user_book_details(username,conn):
    """
    Retrieves book details for a specific user from the database."""
    get_details_query='''SELECT b.title, b.author, b.genre, b.year,b.description FROM books b
                    JOIN borrowedbooks c ON b.id = c.book_id JOIN members m ON c.member_id = m.id WHERE m.name = %s'''
    cur = conn.cursor()
    try:
        cur.execute(get_details_query, (username,))
        book_details = cur.fetchall()
        if book_details:
            # print(f"book details {book_details}")
            df = pd.DataFrame(book_details, columns=['Title', 'Author', 'Genre', 'Published Year', 'Description'])
            # print(f"Book details for {username}:")
            # print(df)
        else:
            print(f"No book details found for user {username}.")
            df=pd.DataFrame()
    except psycopg2.Error as e:
        print(f"get_user_book_details Error retrieving book details: {e}")
    cur.close()
    return df


def create_user(user_Details, conn):
    """
    Creates a new user in the database.
    """
    username = user_Details.get('username')
    email = user_Details.get('email')
    if not username or not email:
        print("Username and email are required to create a user.")
        return False
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO members (username, email) VALUES (%s, %s)", (username, email))
        conn.commit()
        print(f"User {username} created successfully.")
        status = True
    except psycopg2.Error as e:
        print(f"Error creating user: {e}")

        conn.rollback()
        status = False
    finally:
        cur.close()
    return status

def borrow_book(book_name, username, conn):
    """
    Allows a user to borrow a book from the database.
    """
    cur = conn.cursor()
    try:
        # Check if the book exists
        cur.execute("SELECT id FROM books WHERE title = %s", (book_name,))
        book_id = cur.fetchone()
        if not book_id:
            print(f"Book '{book_name}' not found in the database.")
            return False

        # Check if the user exists
        cur.execute("SELECT id FROM members WHERE name = %s", (username,))
        user_id = cur.fetchone()
        if not user_id:
            print(f"User '{username}' not found in the database.")
            return False

        # Insert into borrowedbooks table
        borrwed_date = pd.Timestamp.now()
        cur.execute("INSERT INTO borrowedbooks (book_id, member_id, borrowed_date) VALUES (%s, %s, %s)",
                    (book_id[0], user_id[0], borrwed_date))
        # cur.execute("INSERT INTO borrowedbooks (book_id, member_id) VALUES (%s, %s)", (book_id[0], user_id[0]))
        conn.commit()
        print(f"Book '{book_name}' borrowed successfully by {username}.")
        return True
    except psycopg2.Error as e:
        print(f"Error borrowing book: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()

def recommned_books_based_on_previous_checkouts(username, conn):
    """
    Recommend books based on prevoius checkout using the descriptions of the books"""
    try:
        book_details= get_user_book_details(username, conn)
        if book_details.empty:
            print("No previous checkouts found. Please borrow some books first.")
            return None
        else:
            descriptions = book_details['Description'].tolist()
            genre= book_details['Genre'].tolist()
            if not descriptions:
                print("No descriptions found for previous checkouts.")
                return None
            #for each book description, use description and genre to re
            else:
                print("pass")


    except Exception as e:
        print(f"Error recommending books based on previous checkouts: {e}")
        return None


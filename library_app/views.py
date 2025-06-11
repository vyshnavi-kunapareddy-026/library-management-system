import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.user_utils import authenticate_user
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import connection
from django.contrib.auth.hashers import make_password
from datetime import date

import logging

logger = logging.getLogger(__name__)




def welcome_page(request):
    return render(request, 'welcome.html')

from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.hashers import check_password

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        with connection.cursor() as cursor:
            cursor.execute("SELECT id, password FROM users WHERE username = %s", [username])
            row = cursor.fetchone()

            if row:
                user_id, stored_hashed_password = row  #
                if check_password(password, stored_hashed_password):
                    # Optionally store user info in session
                    request.session['user_id'] = user_id
                    request.session['username'] = username
                    messages.success(request, "Login successful!")
                    return redirect("home")
                else:
                    messages.error(request, "Invalid password.")
            else:
                messages.error(request, "User not found.")

    return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')  # 👈 redirect clears POST and prevents double error on refresh

        # Check if username already exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", [username])
            if cursor.fetchone()[0] > 0:
                messages.error(request, "Username already exists.")
                return redirect('register')

        # Hash and insert
        hashed_password = make_password(password)
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (username, password, full_name, email, phone_number, address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [username, hashed_password, full_name, email, phone_number, address])

        messages.success(request, "Registration successful!")
        return redirect('register')

    return render(request, 'register.html')



def home_view(request):
    return render(request, "home.html")

def get_all_books():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title, author, genre, year, description FROM books ORDER BY title")
        rows = cursor.fetchall()

        books = []
        for row in rows:
            books.append({
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'genre': row[3],
                'year': row[4],
                'description': row[5],
            })

    return books

def view_books(request):
    try:
        books = get_all_books()
        return render(request, "view_books.html", {"books": books})
    except Exception as e:
        logger.error("Failed to retrieve books: %s", str(e))
        messages.error(request, "Failed to retrieve books. Please try again later.")
        return redirect("home")

def borrow_book(request, book_id):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "You must be logged in to borrow a book.")
        return redirect("login")

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO borrowedbooks (book_id, member_id, borrow_date)
                VALUES (%s, %s, %s)
            """, [book_id, user_id, date.today()])
        messages.success(request, "Book borrowed successfully!")
    except Exception as e:
        messages.error(request, f"Failed to borrow book: {str(e)}")

    return redirect("view_books")

def return_book(request):
    return render(request, "return_book.html")

def user_book_log(request):
    return render(request, "user_book_log.html")

def recommend_book(request):
    return render(request, "recommend_book.html")

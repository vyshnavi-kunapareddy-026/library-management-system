import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



from src.user_utils import authenticate_user
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)




def welcome_page(request):
    return render(request, 'welcome.html')

def login_page(request):
    return render(request, "login.html")
    # if request.method == "POST":
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")

    #     try:
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect("home")
    #         else:
    #             messages.error(request, "Invalid username or password.")
    #     except Exception as e:
    #         logger.error("Login failed: %s", str(e))  # logged to console
    #         messages.error(request, "Something went wrong. Please try again.")

    # return render(request, "login.html")

def home_view(request):
    return render(request, "home.html")


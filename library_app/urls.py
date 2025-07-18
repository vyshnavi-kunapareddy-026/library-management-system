from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome'),
    path('login/', views.login_page, name='login'),
    path('home/', views.home_view, name='home'),
    path('books/', views.view_books, name='view_books'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/', views.return_book, name='return_book'),
    path('log/', views.user_book_log, name='user_book_log'),
    path('recommend/', views.recommend_books, name='recommend_books'),
    path('register/', views.register, name='register'),
    path('read/', views.open_library_search, name='open_library_search'),
]

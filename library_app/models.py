from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=50, default='member', null=True)
    phone_number = models.CharField(max_length=15, null=True)
    address = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(null=True)

    class Meta:
        db_table = 'users'
        managed = False  # Important! This prevents Django from trying to create or modify the table.

# Create your models here.
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True)
    author = models.CharField(max_length=255, null=True)
    genre = models.CharField(max_length=100, null=True)
    year = models.IntegerField(null=True)
    description = models.TextField(null=True)

    class Meta:
        db_table = 'books'  # maps to your existing table
        managed = False

class BorrowedBooks(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)  # Now using the real user model
    borrowed_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'borrowedbooks'
        managed = False  # Important! This prevents Django from trying to create or modify the table.
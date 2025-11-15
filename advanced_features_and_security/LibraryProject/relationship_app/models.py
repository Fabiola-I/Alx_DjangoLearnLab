from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# -------------------------------
# Custom User Manager
# -------------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")

        email = self.normalize_email(email)
        if not username:
            username = email

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "Admin")

        return self.create_user(username, email, password, **extra_fields)


# -------------------------------
# CustomUser
# -------------------------------
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Member")

    objects = CustomUserManager()

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


# -------------------------------
# Author
# -------------------------------
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# -------------------------------
# Library
# -------------------------------
class Library(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# -------------------------------
# Librarian (linked to CustomUser)
# -------------------------------
class Librarian(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Librarian: {self.user.username}"


# -------------------------------
# Book
# -------------------------------
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_view", "Can view books"),
            ("can_create", "Can create books"),  # match test exactly
            ("can_edit", "Can edit books"),
            ("can_delete", "Can delete books"),
        ]

    def __str__(self):
        return self.title

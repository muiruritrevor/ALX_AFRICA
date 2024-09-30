from django.db import models
from accounts.models import User
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message="Genre already exists (case insensitive match)"
            ),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])

class Book(models.Model):
    STATUS_CHOICES = [
        ('M', 'Maintenance'),
        ('C', 'Checked out'),
        ('A', 'Available'),
        ('R', 'Reserved'),
    ]

    title = models.CharField(max_length=255, default="Untitled")
    author = models.CharField(max_length=255, blank=True, default="Unknown")
    ISBN = models.CharField(max_length=13, unique=True, blank=True, null=True, verbose_name="ISBN", db_index=True)
    publication_date = models.DateField(null=True, blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    genre = models.ManyToManyField(Genre, blank=True, help_text="Select a genre for this book")
    description = models.TextField(max_length=1000, blank=True, default="No description available")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #created = models.DateTimeField(auto_now_add=True,null=False,blank=False)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='A',
        help_text='Book availability'
    )

    class Meta:
        ordering = ['title', 'author']

    def clean(self):
        if self.available_copies > self.total_copies:
            raise ValidationError("Available copies cannot exceed total copies.")
        if self.total_copies < 0:
            raise ValidationError("Total copies cannot be negative.")
        if self.available_copies < 0:
            raise ValidationError("Available copies cannot be negative.")
    

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def update_status(self):
        if self.available_copies == 0:
            self.status = 'C'
        elif self.available_copies < 3:
            self.status = 'R'
        else:
            self.status = 'A'
        self.save()

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.title} by {self.author or 'Unknown'}"

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def checkout(self, user):
        if self.available_copies > 0:
            self.available_copies -= 1
            if self.available_copies == 0:
                self.status = 'C'
            self.save()
            return Transaction.objects.create(user=user, book=self)
        else:
            raise ValidationError("No available copies to checkout.")

    def return_book(self, transaction):
        if transaction.return_date is None:
            transaction.return_date = timezone.now().date()
            transaction.save()
            self.available_copies += 1
            if self.status == 'C':
                self.status = 'A'
            self.save()
        else:
            raise ValidationError("This book has already been returned.")

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('CO', 'Checkout'),
        ('RT', 'Return'),
        ('RS', 'Reserve'),
        ('CN', 'Cancel Reservation'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=2, choices=TRANSACTION_TYPES, default='CO')
    transaction_date = models.DateTimeField(default=timezone.now, db_index=True)
    due_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    is_overdue = models.BooleanField(default=False)

    class Meta:
        ordering = ['-transaction_date']

    def clean(self):
        if self.return_date and self.return_date < self.transaction_date.date():
            raise ValidationError("Return date cannot be before transaction date.")

    def save(self, *args, **kwargs):
        if self.transaction_type == 'CO' and not self.due_date:
            self.due_date = self.transaction_date.date() + timedelta(days=14)
        
        if self.due_date:
            self.is_overdue = self.return_date is None and timezone.now().date() > self.due_date

        self.full_clean()
        super().save(*args, **kwargs)

    def complete(self):
        if self.return_date:
            raise ValidationError("This book has already been returned.")
        self.return_date = timezone.now()
        self.is_overdue = False
        self.book.available_copies += 1
        self.book.save()
        self.save()

    def cancel_reservation(self):
        """Cancel the reservation and update relevant fields."""
        self.return_date = None
        self.is_overdue = False  # Reset overdue status
        self.save()

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.book.title} by {self.user.username} on {self.transaction_date.date()}"
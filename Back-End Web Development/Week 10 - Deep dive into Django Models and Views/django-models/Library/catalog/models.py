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
    available_copies = models.PositiveIntegerField(default=0)
    genre = models.ManyToManyField(Genre, blank=True, help_text="Select a genre for this book")
    description = models.TextField(max_length=1000, blank=True, default="No description available")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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
        """Create a string for the Genre."""
        return ', '.join(genre.name for genre in self.genre.all())
    
    display_genre.short_description = 'Genre'
    
    @property
    def genre_list(self):
        """Return a list of genre IDs for this book."""
        return list(self.genre.values_list('id', flat=True))

    def borrow(self, user):
        return BorrowedBook.create_borrowed_book(user, self)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    returned_date = models.DateField(null=True, blank=True)
    is_overdue = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user.username} on {self.borrowed_date}"
    

    def save(self, *args, **kwargs):
        # Ensure borrowed_date is not None
        if self.borrowed_date:
            # Set the due_date if it doesn't exist
            if not self.due_date:
                self.due_date = self.borrowed_date.date() + timedelta(days=14)

            # Convert timezone.now() to date for comparison
            current_date = timezone.now().date()

            # Check if the book is overdue
            self.is_overdue = self.returned_date is None and current_date > self.due_date

        # Call the parent save method to save the instance
        super().save(*args, **kwargs)

    def return_book(self):
        if self.returned_date:
            raise ValidationError("This book has already been returned.")
        self.returned_date = timezone.now().date()
        self.is_overdue = False
        self.book.available_copies += 1
        self.book.update_status()
        self.save()

    @property
    def is_active(self):
        return self.returned_date is None

    @classmethod
    def create_borrowed_book(cls, user, book):
        if book.available_copies > 0:
            borrowed_book = cls(user=user, book=book)
            book.available_copies -= 1
            book.update_status()
            borrowed_book.save()
            return borrowed_book
        else:
            raise ValidationError("No available copies to borrow.")

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('CO', 'Checkout'),
        ('RT', 'Return'),
        ('RS', 'Reserve'),
        ('CN', 'Cancel Reservation'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    borrowed_book = models.OneToOneField(BorrowedBook, on_delete=models.SET_NULL, null=True, blank=True, related_name='transaction')
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
        if self.transaction_type == 'CO':
            if not self.borrowed_book:
                self.borrowed_book = BorrowedBook.create_borrowed_book(self.user, self.book)
            if not self.due_date:
                self.due_date = self.transaction_date.date() + timedelta(days=14)
        
        self.is_overdue = self.return_date is None and self.due_date and timezone.now().date() > self.due_date

        self.full_clean()
        super().save(*args, **kwargs)

    def complete(self):
        if self.return_date:
            raise ValidationError("This transaction has already been completed.")
        self.return_date = timezone.now().date()
        self.is_overdue = False
        if self.borrowed_book:
            self.borrowed_book.return_book()
        self.save()

    def cancel_reservation(self):
        if self.transaction_type != 'RS':
            raise ValidationError("Only reservations can be canceled.")
        self.return_date = timezone.now().date()
        self.is_overdue = False
        self.save()

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.book.title} by {self.user.username} on {self.transaction_date.date()}"
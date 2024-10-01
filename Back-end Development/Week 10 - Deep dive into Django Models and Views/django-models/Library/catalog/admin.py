from django.contrib import admin
from .models import Book, Transaction, BorrowedBook

# Inline for Transactions within Book Admin
class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0  # No extra empty fields
    readonly_fields = ('transaction_date', 'due_date', 'is_overdue')  # Making non-editable fields read-only

    # Exclude fields that aren't necessary in the inline form
    exclude = ('transaction_type',)

# Admin class for Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'ISBN', 'status', 'total_copies', 'available_copies', 'created_by')
    list_filter = ('status', 'author')  # Filter options for status and author
    search_fields = ('title', 'author__name', 'ISBN')  # Search options for title, author, and ISBN
    inlines = [TransactionInline]  # Display related transactions inline

    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'ISBN', 'publish_date', 'status', 'created_by')
        }),
        ('Copies', {
            'fields': ('total_copies', 'available_copies')
        }),
    )

# Admin class for Transaction
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'transaction_type', 'transaction_date', 'due_date', 'is_overdue')
    list_filter = ('book', 'user')  # Filter by book or user involved in the transaction
    search_fields = ('user__username', 'book__title')  # Search by username or book title

    readonly_fields = ('transaction_date', 'due_date', 'is_overdue')  # Non-editable fields

    fieldsets = (
        (None, {
            'fields': ('user', 'book', 'transaction_type')  # Exclude non-editable fields
        }),
    )

# Admin class for BorrowedBook (assuming this tracks individual borrowed instances)
@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_date', 'due_date', 'returned_date', 'is_overdue')
    list_filter = ('user', 'book')  # Filter by the borrower or book
    search_fields = ('user', 'title')  # Search by borrower username or book title

    readonly_fields = ('borrowed_date', 'due_date', 'returned_date', 'is_overdue')  # Non-editable fields

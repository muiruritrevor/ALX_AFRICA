from django.contrib import admin
from .models import Book, Transaction

# Inline for Transactions within Book Admin
class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0  
    exclude = ('transaction_date', 'due_date', 'is_overdue')

# Admin class for Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'ISBN', 'status', 'total_copies', 'available_copies', 'created_by')
    list_filter = ('status', 'author')  # Filter options for status and author
    search_fields = ('title', 'author', 'ISBN')  # Search options for title, author, and ISBN
    inlines = [TransactionInline]  # Display related transactions inline

    # Display Genre in Book list, assuming you have a ManyToMany field for Genre
    # list_display = ('title', 'author', 'display_genre')  

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
    list_display = ('user', 'book', 'transaction_type', 'transaction_date', 'is_overdue') # Show checkout_date
    list_filter = ('book', 'user')
    search_fields = ('user__username', 'book__title')  # Search by username or book title

    # Fieldsets to exclude non-editable fields
    fieldsets = (
        (None, {
            'fields': ('user', 'book')  # Exclude checkout_date from form
        }),
    )

    readonly_fields = ('transaction_date',) 
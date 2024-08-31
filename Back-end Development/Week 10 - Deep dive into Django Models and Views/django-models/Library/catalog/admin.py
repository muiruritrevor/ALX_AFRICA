from django.contrib import admin

from .models import Genre, Author, Book, Library, Librarian, BookInstance

# admin.site.register(Genre)
# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(Library)
# admin.site.register(Librarian)
# admin.site.register(BookInstance)

# @admin.register(Genre)
# class Genre(admin.ModelAdmin):
#     list_display = ('genre')
#     inlines = [Genre]
admin.site.register(Genre)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth',)
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
admin.site.register(Author, AuthorAdmin)

# Register the Admin classes for Book usong the decorator
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

# Register the Admin classes for Bookinstaance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book', 'status', 'due_back', 'id')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

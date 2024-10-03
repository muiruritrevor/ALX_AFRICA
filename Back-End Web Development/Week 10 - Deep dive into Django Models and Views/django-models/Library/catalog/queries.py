from catalog.models import Author, Book, Library, Librarian

def query_all_books(author):
    return Book.objects.filter(author)
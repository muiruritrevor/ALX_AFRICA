from django.shortcuts import render
from .models import Genre, Author, Book, BookInstance, Library, Librarian

def index(request):
    """View functionfor home page of site."""

    # Generate counts of some of the main object
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()

    num_authors = Author.objects.count()

    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_author' : num_authors,
    }

    return render(request, 'index.html', context = context)
# Create your views here.

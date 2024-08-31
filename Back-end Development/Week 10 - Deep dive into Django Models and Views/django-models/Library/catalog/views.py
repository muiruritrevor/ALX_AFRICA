from django.shortcuts import render
from django.views import generic
from .models import Genre, Author, Book, BookInstance, Library, Librarian

def index(request):
    """View function for home page of site."""

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

    return render(request, 'catalog/index.html', context = context)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    #queryset = Book.objects.filter(title__icontains='')[:5] 
    template_name = 'books/book_list.html'

class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book_detail'
    template_name = 'books/book_detail.html'
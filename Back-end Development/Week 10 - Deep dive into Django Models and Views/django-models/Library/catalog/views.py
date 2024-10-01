from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from .models import Book, Transaction, Genre, BorrowedBook
from .serializers import BookSerializer, TransactionSerializer
from .forms import BookForm
from .permissions import IsLibrarianOrReadOnly


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@login_required
def dashboard(request):
    # Get the user's currently borrowed books
    current_borrowed_books = BorrowedBook.objects.filter(user=request.user, returned_date__isnull=True)
    
    # Get the total number of books the user has borrowed
    total_borrowed = BorrowedBook.objects.filter(user=request.user).count()
    
    # Get the user's favorite genres (top 3)
    favorite_genres = BorrowedBook.objects.filter(user=request.user) \
        .values('book__genre') \
        .annotate(count=Count('book__genre')) \
        .order_by('-count')[:3]
    
    # Get books due soon (within 7 days)
    from datetime import timedelta
    from django.utils import timezone
    books_due_soon = current_borrowed_books.filter(
        due_date__lte=timezone.now() + timedelta(days=7)
    )
    
    context = {
        'current_borrowed_books': current_borrowed_books,
        'total_borrowed': total_borrowed,
        'favorite_genres': favorite_genres,
        'books_due_soon': books_due_soon,
    }
    
    return render(request, 'catalog/dashboard.html', context)

@login_required
def index_view(request):
    """View function for home page of the site."""
    available_books = Book.objects.filter(available_copies__gt=0).order_by('title')
    context = {
        'available_books': available_books,
    }
    return render(request, 'catalog/index.html', context=context)

@login_required
def reading_history(request):
    # Get all books borrowed by the user, ordered by borrow date
    history = BorrowedBook.objects.filter(user=request.user).order_by('-borrowed_date')

    # Create a list to hold the reading history with transaction status
    reading_history_with_status = []
    
    for record in history:
        reading_history_with_status.append({
            'book': record.book,
            'borrowed_date': record.borrowed_date,
            'returned_date': record.returned_date,
            'status': 'Returned' if record.returned_date else 'Checked Out',
        })

    context = {
        'reading_history': reading_history_with_status,
    }
    
    return render(request, 'catalog/reading_history.html', context)


@login_required
def recommendations(request):
    # Get user's favorite genres
    favorite_genres = BorrowedBook.objects.filter(user=request.user) \
        .values('book__genre') \
        .annotate(count=Count('book__genre')) \
        .order_by('-count')[:3]
    
    favorite_genre_names = [genre['book__genre'] for genre in favorite_genres]
    
    # Get books in user's favorite genres that they haven't borrowed yet
    recommended_books = Book.objects.filter(genre__in=favorite_genre_names) \
        .exclude(borrowedbook__user=request.user) \
        .distinct()[:10]
    
    # Get popular books across all users
    popular_books = Book.objects.annotate(borrow_count=Count('borrowedbook')) \
        .order_by('-borrow_count')[:5]
    
    context = {
        'recommended_books': recommended_books,
        'popular_books': popular_books,
    }
    
    return render(request, 'catalog/recommendations.html', context)
  
@login_required
def add_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            # form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Book added successfully!')
            return redirect('add_book_view')
    else:
        form = BookForm()
    
    books = Book.objects.all().order_by('-id')
    return render(request, 'catalog/add_book.html', {'form': form, 'books': books})

@login_required
def edit_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('add_book_view')
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'catalog/edit_book.html', context)

@login_required
def delete_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('index')
    context = {
        'book': book,
    }
    return render(request, 'catalog/delete_book.html', context)

@login_required
def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_transaction = Transaction.objects.filter(user=request.user, book=book, return_date__isnull=True).first()
    context = {
        'book': book,
        'user_transaction': user_transaction,
    }
    return render(request, 'catalog/book_detail.html', context)

@login_required
def book_list_view(request):
    books = Book.objects.all()  # Retrieve all books from the database
    context = {
        'books': books,
    }
    return render(request, 'catalog/book_list.html', context)

@login_required
def check_out_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.available_copies > 0:
        Transaction.objects.create(user=request.user, book=book)
        book.available_copies -= 1
        book.save()
        messages.success(request, f"You've successfully checked out '{book.title}'.")
    else:
        messages.error(request, "No copies available to check out.")
    return redirect('add_book_view')

@login_required
def return_book_view(request, transaction_id):
    transaction_instance = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    if transaction_instance.return_date:
        messages.error(request, "This book has already been returned.")
    else:
        with transaction.atomic():
            transaction_instance.return_date = timezone.now()
            transaction_instance.book.available_copies += 1
            transaction_instance.book.save()
            transaction_instance.save()
        messages.success(request, f"You've successfully returned '{transaction_instance.book.title}'.")

        # Here we will add the transaction to the user's reading history if it's not already reflected.
        # This can also be handled in the reading history view, depending on how you are managing the data.
        # Assuming that reading history is based on BorrowedBook model:
        BorrowedBook.objects.filter(user=request.user, book=transaction_instance.book, returned_date__isnull=True).update(returned_date=timezone.now())

    return redirect('book_detail_view', book_id=transaction_instance.book.id)

@login_required
def user_transactions_view(request):
    """View function to display a user's transaction history."""
    # Retrieve all transactions for the current user
    transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')  # Adjust based on your model's field names
    context = {
        'transactions': transactions,
    }
    return render(request, 'catalog/user_transactions.html', context)

# DRF ViewSets (for API interactions)
class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for managing books via API."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsLibrarianOrReadOnly]
    pagination_class = StandardResultsSetPagination


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing transactions via API."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if book.available_copies <= 0:
            raise serializers.ValidationError("No copies available to check out.")
        book.available_copies -= 1
        book.save()
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        transaction = self.get_object()
        if transaction.return_date:
            raise serializers.ValidationError("This book has already been returned.")
        if 'return_date' in serializer.validated_data:
            book = transaction.book
            book.available_copies += 1
            book.save()
        serializer.save()


# DRF API views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_book_list(request):
    """API endpoint to list available books."""
    books = Book.objects.filter(available_copies__gt=0).order_by('title')
    paginator = StandardResultsSetPagination()
    paginated_books = paginator.paginate_queryset(books, request)
    serializer = BookSerializer(paginated_books, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_book_detail(request, pk):
    """API endpoint to retrieve book details."""
    book = get_object_or_404(Book, pk=pk)
    serializer = BookSerializer(book)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_check_out_book(request, book_id):
    """API endpoint to check out a book."""
    book = get_object_or_404(Book, id=book_id)
    if book.available_copies <= 0:
        return Response({"error": "No copies available to check out."}, status=status.HTTP_400_BAD_REQUEST)

    transaction = Transaction(user=request.user, book=book)
    with transaction.atomic():
        transaction.save()
        book.available_copies -= 1
        book.save()

    return Response({"message": "Book checked out successfully."}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_return_book(request, transaction_id):
    """API endpoint to return a checked-out book."""
    transaction_instance = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    if transaction_instance.return_date:
        return Response({"error": "This book has already been returned."}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        # Mark the book as returned by setting the return date
        transaction_instance.return_date = timezone.now()
        # Increment the available copies
        transaction_instance.book.available_copies += 1
        transaction_instance.book.save()
        transaction_instance.save()

    return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_transaction_history(request):
    """API endpoint to retrieve user's transaction history."""
    transactions = Transaction.objects.filter(user=request.user)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

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
from .models import Book, Transaction, BorrowedBook
from .serializers import BookSerializer, TransactionSerializer
from .forms import BookForm


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@login_required
def dashboard(request):
    """
    Display user's dashboard with borrowed books, total borrowed, favorite genres, and due dates.
    """
    current_borrowed_books = BorrowedBook.objects.filter(user=request.user, returned_date__isnull=True)
    total_borrowed = BorrowedBook.objects.filter(user=request.user).count()
    favorite_genres = BorrowedBook.objects.filter(user=request.user) \
        .values('book__genre') \
        .annotate(count=Count('book__genre')) \
        .order_by('-count')[:3]
    books_due_soon = current_borrowed_books.filter(
        due_date__lte=timezone.now() + timezone.timedelta(days=7)
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
    """Display home page with available books."""
    available_books = Book.objects.filter(available_copies__gt=0).order_by('title')
    return render(request, 'catalog/index.html', {'available_books': available_books})

@login_required
def reading_history(request):
    """Display user's reading history."""
    history = BorrowedBook.objects.filter(user=request.user).order_by('-borrowed_date')
    reading_history_with_status = [{
        'book': record.book,
        'borrowed_date': record.borrowed_date,
        'returned_date': record.returned_date,
        'status': 'Returned' if record.returned_date else 'Checked Out',
    } for record in history]
    
    return render(request, 'catalog/reading_history.html', {'reading_history': reading_history_with_status})

@login_required
def recommendations(request):
    """Provide book recommendations based on user's favorite genres and popular books."""
    favorite_genres = BorrowedBook.objects.filter(user=request.user) \
        .values('book__genre') \
        .annotate(count=Count('book__genre')) \
        .order_by('-count')[:3]
    
    favorite_genre_names = [genre['book__genre'] for genre in favorite_genres]
    
    recommended_books = Book.objects.filter(genre__in=favorite_genre_names) \
        .exclude(borrowedbook__user=request.user) \
        .distinct()[:10]
    
    popular_books = Book.objects.annotate(borrow_count=Count('borrowedbook')) \
        .order_by('-borrow_count')[:5]
    
    context = {
        'recommended_books': recommended_books,
        'popular_books': popular_books,
    }
    
    return render(request, 'catalog/recommendations.html', context)

@login_required
def manage_book(request, book_id=None):
    book = get_object_or_404(Book, id=book_id) if book_id else None
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            if not book_id:
                book.created_by = request.user
            book.save()
            messages.success(request, f"Book {'updated' if book_id else 'added'} successfully!")
            return redirect('manage_book')
    else:
        form = BookForm(instance=book)
    
    books = Book.objects.all().order_by('-id')
    context = {'form': form, 'books': books, 'book': book}
    return render(request, 'catalog/manage_book.html', context)

@login_required
def delete_book_view(request, book_id):
    """Delete a book."""
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('index')
    return render(request, 'catalog/delete_book.html', {'book': book})

@login_required
def book_detail_view(request, book_id):
    """Display book details and user's transaction status for the book."""
    book = get_object_or_404(Book, id=book_id)
    user_transaction = Transaction.objects.filter(user=request.user, book=book, return_date__isnull=True).first()
    return render(request, 'catalog/book_detail.html', {'book': book, 'user_transaction': user_transaction})

@login_required
def book_list_view(request):
    """Display a list of all books."""
    books = Book.objects.all()
    return render(request, 'catalog/book_list.html', {'books': books})

@login_required
def check_out_book(request, book_id):
    """Check out a book."""
    book = get_object_or_404(Book, id=book_id)
    if book.available_copies > 0:
        with transaction.atomic():
            Transaction.objects.create(user=request.user, book=book)
            book.available_copies -= 1
            book.save()
            BorrowedBook.objects.create(user=request.user, book=book, borrowed_date=timezone.now())
        messages.success(request, f"You've successfully checked out '{book.title}'.")
    else:
        messages.error(request, "No copies available to check out.")
    return redirect('book_detail_view', book_id=book_id)

@login_required
def return_book(request, transaction_id):
    """Return a checked out book."""
    transaction_instance = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    if transaction_instance.return_date:
        messages.error(request, "This book has already been returned.")
    else:
        with transaction.atomic():
            transaction_instance.return_date = timezone.now()
            transaction_instance.book.available_copies += 1
            transaction_instance.book.save()
            transaction_instance.save()
            BorrowedBook.objects.filter(user=request.user, book=transaction_instance.book, returned_date__isnull=True).update(returned_date=timezone.now())
        messages.success(request, f"You've successfully returned '{transaction_instance.book.title}'.")

    return redirect('book_detail_view', book_id=transaction_instance.book.id)

@login_required
def user_transactions_view(request):
    """Display user's transaction history."""
    transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')
    return render(request, 'catalog/user_transactions.html', {'transactions': transactions})

# DRF ViewSets (for API interactions)
class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for managing books via API."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
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

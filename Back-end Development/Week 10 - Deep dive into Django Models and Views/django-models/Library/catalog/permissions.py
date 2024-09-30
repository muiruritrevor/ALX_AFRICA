from rest_framework import permissions, viewsets
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer

class IsLibrarianOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

# Update ViewSets
class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsLibrarianOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

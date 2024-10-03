from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from accounts.views import login_view, register, profile, logout_view

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'transactions', views.TransactionViewSet, basename='transaction')

urlpatterns = [
    # Django template-based URLs
    path('', views.index_view, name='index'),  # Home page view
    path('dashboard/', views.dashboard, name='dashboard'),
    path('books/', views.book_list_view, name='book_list'),
    path('books/manage/', views.manage_book, name='manage_book'),
    path('books/manage/<int:book_id>/', views.manage_book, name='manage_book'),
    path('books/delete/<int:book_id>/', views.delete_book_view, name='delete_book_view'),
    path('books/<int:book_id>/', views.book_detail_view, name='book_detail_view'),
    path('books/checkout/<int:book_id>/', views.check_out_book, name='check_out_book'),
    path('books/return/<int:transaction_id>/', views.return_book, name='return_book'),
    path('transactions/', views.user_transactions_view, name='user_transactions_view'),
    path('reading-history/', views.reading_history, name='reading_history'),
    path('recommendations/', views.recommendations, name='recommendations'),
    
    # DRF API URLs
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/', include(router.urls)),  # This will include the registered viewsets
    path('api/books/', views.api_book_list, name='api_book_list'),
    path('api/books/<int:pk>/', views.api_book_detail, name='api_book_detail'),
    path('api/check-out/<int:book_id>/', views.api_check_out_book, name='api_check_out_book'),
    path('api/return/<int:transaction_id>/', views.api_return_book, name='api_return_book'),
    path('api/history/', views.api_transaction_history, name='api_transaction_history'),
]
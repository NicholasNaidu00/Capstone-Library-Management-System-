from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Book, Transaction
from .serializers import BookSerializer, TransactionSerializer, UserSerializer
from django.contrib.auth.models import User

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Book.objects.all()
        available = self.request.query_params.get('available', None)
        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)
        isbn = self.request.query_params.get('isbn', None)

        if available:
            queryset = queryset.filter(copies_available__gt=0)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if isbn:
            queryset = queryset.filter(isbn=isbn)

        return queryset

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        book_id = request.data.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        if book.copies_available <= 0:
            return Response(
                {"error": "No copies available for checkout"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user already has this book checked out
        existing_checkout = Transaction.objects.filter(
            user=request.user,
            book=book,
            is_returned=False
        ).first()

        if existing_checkout:
            return Response(
                {"error": "You already have this book checked out"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            book.copies_available -= 1
            book.save()

            transaction_obj = Transaction.objects.create(
                user=request.user,
                book=book,
                transaction_type='checkout'
            )

        serializer = self.get_serializer(transaction_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def return_book(self, request):
        book_id = request.data.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        transaction_obj = get_object_or_404(
            Transaction,
            user=request.user,
            book=book,
            is_returned=False
        )

        with transaction.atomic():
            book.copies_available += 1
            book.save()

            transaction_obj.is_returned = True
            transaction_obj.return_date = timezone.now()
            transaction_obj.save()

        serializer = self.get_serializer(transaction_obj)
        return Response(serializer.data)

from datetime import timedelta
from django.utils import timezone

from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .permissions import IsProductOwner
from .models import Product, Category, ProductImage
from .serializers import ProductSerializer, CategorySerializer, ProductImageSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser, ]

    def get_permissions(self):          #cutting permissions
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsProductOwner, ]
        else:
            permissions = [IsAuthenticated, ]

        return [permission() for permission in permissions]

#filtration
    def get_queryset(self):
        queryset = super().get_queryset()
        days_count = int(self.request.query_params.get('day', 0))
        if days_count > 0:
            start_date = timezone.now() - timedelta(days=days_count)
            queryset = queryset.filter(created_at__gte=start_date)
        return queryset

#for search

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(body__icontains=q))
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductImageView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}
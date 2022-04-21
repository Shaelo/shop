from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet

from applications.product.serializers import CategorySerializer
from applications.product.filters import ProductFilter
from applications.product.models import Product, Rating, Category
from applications.product.permissions import IsAdmin, IsAuthor
from applications.product.serializers import ProductSerializer, RatingSerializers


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filter_fields = ['category', 'owner']
    filterset_class = ProductFilter
    ordering_fields = ['id', 'price']
    search_fields = ['name', 'description']

    def get_permissions(self):
        print(self.action)
        if self.action in ['list', 'retrieve']:
            permissions = []
        elif self.action == 'rating':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # .../rating/2/
    @action(methods=['POST'], detail=True)
    def rating(self, request, pk): # http://localhost:8000/product/id_product/rating/
        serializer = RatingSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj = Rating.objects.get(product=self.get_object(),
                                     owner=request.user)
            obj.rating = request.data['rating']
        except Rating.DoesNotExist:
            obj = Rating(owner=request.user,
                         product=self.get_object(),
                         rating= request.data['rating']
                        )
        obj.save()
        return Response(request.data,
                        status=status.HTTP_201_CREATED)


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryRetriveDeleteUpdateView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]




# class ListCreateView(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # permission_classes = [IsAuthenticatedOrReadOnly] # IsAdminUser
#     # pagination_class = None
#     pagination_class = LargeResultsSetPagination
#
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_fields = ['category', 'price']
#     # search_fields = ['name', 'description']
#     # filterset_class = ProductFilter
#     ordering_fields = ['id']
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         search = self.request.query_params.get('search')
#         if search:
#             queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))
#         return queryset
#
#
# class DeleteUpdateRetriveView(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthor]   # [IsAdmin]


# class ProductViewSet(ListModelMixin, CreateModelMixin , RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin ,GenericViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class ProductViewSet(ViewSet):
#     def list(self, request):
#         pass
#     def create(self):
#         pass
#     def retrieve(self):
#         pass
#     def update(self):
#         pass
#     def destroy(self):
#         pass
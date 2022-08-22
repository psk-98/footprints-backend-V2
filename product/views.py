from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view

from order import serializers

from .pagination import CustomPagination

from django.db.models import Q

from django.http import Http404

from .models import Product, ProductImage, ProductStock
from .serializers import ProductImageSerializer, ProductSerializer, StockSerializer

class ProductsView(APIView, CustomPagination):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()

        if request.query_params.get('sort'):
            sort = request.query_params.get('sort')
            products = products.order_by(sort)

        if request.query_params.get('category'):
            category = request.query_params.get('category')
            print(category)
            products = products.filter(category=category)

        
        if request.query_params.get('filterToPrice'):
            toPrice = request.query_params.get('filterToPrice')
            products = products.filter(price__lte=toPrice)

        if request.query_params.get('filterFromPrice'):
            fromPrice = request.query_params.get('filterFromPrice')
            products = products.filter(price__gte=fromPrice)

        if request.query_params.get('search'):
            search = request.query_params.get('search')
            products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))

        #if request.query_params.get('sizes')

        results = self.paginate_queryset(products, request, view=self)

        serializer = ProductSerializer(results, many=True)

        return self.get_paginated_response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
    

class ProductView(APIView):
    
    def get(self, request):
        try: 
            product = Product.objects.get(slug=request.query_params.get('slug'))
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class StockView(APIView):

    def get(self, request):
        stock = ProductStock.objects.all()
        serializer = StockSerializer(stock, many=True)
        return Response(serializer.data)

    def post(self, request):
        print(request.data['user'])
        serializer = StockSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data)


####temp views

class CreateProduct(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class UploadImage(generics.CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class CreateStock(generics.CreateAPIView):
    queryset = ProductStock.objects.all()
    serializer_class = StockSerializer

@api_view(['POST'])
def upload_stock(request):
    
    for stock in request.data:
        print(stock)
        size = stock['size']
        amount_in_stock = stock['amount_in_stock']
        product = Product.objects.get(id=stock['product'])
        ProductStock.objects.create(product=product,
                                    size=size,
                                    amount_in_stock=amount_in_stock)

    Response({"result":"was created" },status=status.HTTP_201_CREATED)



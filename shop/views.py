from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


from .models import Product
from .serializers import ProductSerializer


class ProductView(APIView):
    """ Информация о продукте по его идентификатору """
    renderer_classes = [JSONRenderer]

    def get(self, request, pk):
        return Response(ProductSerializer(Product.objects.get(pk=pk)).data)


class ProductListView(ListAPIView):
    """ Список продуктов с поиском по полям Артикул и Название и фильтром по статусу """

    serializer_class = ProductSerializer
    renderer_classes = [JSONRenderer]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['state']  # todo: надо наверно как-то из Product получить название поля
    search_fields = ['sku', 'title']

    def get_queryset(self):
        return Product.objects.get_queryset()

    def get(self, request: Request, **kwargs):
        return self.list(request, **kwargs)

import django_filters
from Product.models import products

class ProductFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='Category')

    class Meta:
        model = products
        fields = ['category']
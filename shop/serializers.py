from rest_framework.serializers import ModelSerializer

from .models import Product
from .helpers import split_file_to_path_and_format


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.image:
            representation['image'] = None
        else:
            image_url = instance.image.url
            img_url_without_format, img_format = split_file_to_path_and_format(image_url)
            formats = {img_format, 'webp'}
            representation['image'] = {'path': img_url_without_format, 'formats': list(formats)}

        return representation
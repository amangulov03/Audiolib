from rest_framework import serializers

from .models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        exclude = ('user', )

    def validate(self, attrs):
        super().validate(attrs)
        attrs['user'] = self.context['request'].user
        if Favorite.objects.filter(user=attrs["user"], book=attrs["book"]).exists():
            raise serializers.ValidationError("Эта книга уже есть в избранном")
        return attrs
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['book'] = {
            'id': instance.book.id,
            'title': instance.book.title,
            'cover_image': instance.book.cover_image.url,
            'author': instance.book.author
        }
        return repr

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['user', 'book']

    def validate(self, data):
        user = self.context['request'].user
        book_id = self.context['view'].kwargs.get('book_id')
        if book_id and Review.objects.filter(user=user, book_id=book_id).exists():
            raise ValidationError("Вы уже оставили отзыв на эту книгу")
        return data


    def to_representation(self, instance):
        repr =   super().to_representation(instance)
        repr['user'] = {
            'id':instance.user.id,
            'email': instance.user.email
        }
        return repr
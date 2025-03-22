from rest_framework import serializers
from .models import Wish


class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ['id', 'title', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

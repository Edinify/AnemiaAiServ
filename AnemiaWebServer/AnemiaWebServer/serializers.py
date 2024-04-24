from rest_framework import serializers
from .models import Test, Post

class TestSerializer(serializers.ModelSerializer):
  class Meta:
    model = Test
    fields = ["id","name","description"] 

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
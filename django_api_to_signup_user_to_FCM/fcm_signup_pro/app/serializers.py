from rest_framework import serializers

class SignupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=243)
    email = serializers.EmailField(max_length=243)
    password = serializers.CharField(max_length=243)
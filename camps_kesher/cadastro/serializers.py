from rest_framework import serializers
from .models import Usuario, Fisico
from django.contrib.auth.password_validation import validate_password

class FisicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fisico
        fields = "__all__"
class UsuarioSerializer(serializers.ModelSerializer):
    fisico = FisicoSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "username", "first_name", "last_name",
                  "idade", "email", "telefone", "tipo", "fisico"]

class UsuarioCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "username", "first_name", "last_name",
                  "idade", "email", "telefone", "tipo", "password"]

    def create(self, validated_data):
        user = Usuario(
            username=validated_data.get("username"),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            idade=validated_data.get("idade"),
            email=validated_data.get("email"),
            telefone=validated_data.get("telefone"),
            tipo=validated_data.get("tipo", "aluno"),
        )
        user.set_password(validated_data.get("password"))
        user.save()
        return user
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
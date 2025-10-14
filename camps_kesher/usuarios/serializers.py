from rest_framework import serializers
from .models import Usuario, Fisico

class FisicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fisico
        fields = "__all__"

class UsuarioSerializer(serializers.ModelSerializer):
    fisico = FisicoSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "username", "first_name", "last_name", "email", "data_de_nascimento", "telefone", "fisico"]

class UsuarioCreateSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "username", "first_name", "last_name", "email", "data_de_nascimento", "telefone", "senha"]

    def create(self, validated_data):
        user = Usuario(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            data_de_nascimento=validated_data.get("data_de_nascimento"),
            telefone=validated_data.get("telefone"),
        )
        user.set_password(validated_data["senha"])
        user.save()
        return user
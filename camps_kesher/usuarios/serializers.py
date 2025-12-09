from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Fisico

class FisicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fisico
        fields = ["data_de_nascimento", "telefone", "objetivo", "peso", "altura"]

class UsuarioSerializer(serializers.ModelSerializer):
    fisico = FisicoSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "fisico"]

class UsuarioCreateSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)
    
    data_de_nascimento = serializers.DateField(write_only=True, required=False)
    telefone = serializers.CharField(write_only=True, required=False)
    objetivo = serializers.CharField(write_only=True, required=False)
    peso = serializers.DecimalField(max_digits=6, decimal_places=2, write_only=True, required=False)
    altura = serializers.DecimalField(max_digits=4, decimal_places=2, write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "senha",
            "data_de_nascimento",
            "telefone",
            "objetivo",
            "peso",
            "altura"
        ]

    def create(self, validated_data):
        fisico_data = {
            "data_de_nascimento": validated_data.pop("data_de_nascimento", None),
            "telefone": validated_data.pop("telefone", None),
            "objetivo": validated_data.pop("objetivo", None),
            "peso": validated_data.pop("peso", None),
            "altura": validated_data.pop("altura", None),
        }

        senha = validated_data.pop("senha")

        user = User(**validated_data)
        user.set_password(senha)
        user.save()

        Fisico.objects.create(
            user=user,
            **fisico_data
        )

        return user

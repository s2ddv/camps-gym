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
        fields = ["id", "username", "first_name", "last_name",
"idade", "email", "telefone", "fisico"]

class UsuarioCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "username", "first_name", "last_name",
"idade", "email", "telefone", "password"]
        
    def create(self, validated_data):
        user = Usuario(
            username=validated_data["Nome de Usuário"],
            first_name = validated_data.get("Primeiro Nome", ""),
            last_name = validated_data.get("Último Nome", ""),
            idade = validated_data.get("Idade"),
            email = validated_data.get("Email"),
            telefone = validated_data.get("Telefone"),
        )
        user .set_password(validated_data["Senha"])
        user.save()
        return user
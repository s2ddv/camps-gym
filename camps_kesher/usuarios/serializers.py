from rest_framework import serializers
from .models import Usuario, Fisico

class FisicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fisico
        fields = "__all__"
class UsuarioSerializer(serializers.ModelSerializer):
    físico = FisicoSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = ["id", "nome_de_usuário","primeiro_nome", "último_nome", "email", "data_de_nascimento", "telefone", "fisico"]

        class UsuarioCreateSerializer(serializers.ModelSerializer):
            password = serializers.CharField(write_only=True)

            class Meta:
                model = Usuario
                fields = ["id", "nome_de_usuário","primeiro_nome", "último_nome", "email", "data_de_nascimento", "telefone", "senha"]

            def create(self, validated_data):
                user = Usuario(
                    nome_de_usuario=validated_data["nome_de_usuário"],
                    primeiro_nome=validated_data["primeiro_nome"],
                    ultimo_nome=validated_data["último_nome"],
                    email=validated_data["email"],
                    data_de_nascimento=validated_data.get("data_de_nascimento"),
                    telefone=validated_data.get("telefone"),
                )
                user.set.password(validated_data["senha"])
                user.save()
                return user
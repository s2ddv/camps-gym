from rest_framework import serializers
from .models import Categoria, Produto, ProdutoVariacao, Tamanho


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class TamanhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tamanho
        fields = '__all__'


class ProdutoVariacaoSerializer(serializers.ModelSerializer):
    tamanho = TamanhoSerializer(read_only=True)
    tamanho_id = serializers.PrimaryKeyRelatedField(
        queryset=Tamanho.objects.all(),
        source='tamanho',
        write_only=True
    )

    class Meta:
        model = ProdutoVariacao
        fields = ['id', 'cor', 'tamanho', 'tamanho_id', 'estoque']


class ProdutoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',
        write_only=True
    )

    variacoes = ProdutoVariacaoSerializer(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = '__all__'

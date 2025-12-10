from rest_framework import serializers
from .models import Categoria, Produto, ProdutoVariacao, Tamanho
from django.core.exceptions import ObjectDoesNotExist


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


class ProdutoComVariacaoSerializer(serializers.Serializer):
    produto_id = serializers.IntegerField()
    cor = serializers.CharField()
    tamanho = serializers.CharField()
    estoque = serializers.IntegerField()

    def validate_tamanho(self, value):
        
        label_to_value = {label.lower(): val for val, label in Tamanho.TAMANHO}

       
        value_to_value = {val.lower(): val for val, label in Tamanho.TAMANHO}

        key = value.lower()

        if key in value_to_value:
            return value_to_value[key]   

        if key in label_to_value:
            return label_to_value[key]  

        raise serializers.ValidationError("Tamanho inválido.")

    def create(self, validated_data):
        produto = Produto.objects.get(id=validated_data["produto_id"])
        tamanho_valor = validated_data["tamanho"] 
        tamanho_obj = Tamanho.objects.get(nome=tamanho_valor)

        variacao = ProdutoVariacao.objects.create(
            produto=produto,
            cor=validated_data["cor"],
            tamanho=tamanho_obj,
            estoque=validated_data["estoque"],
        )

        return variacao

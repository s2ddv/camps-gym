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

    def create(self, validated_data):
        produto = Produto.objects.get(id=validated_data['produto_id'])
        print("Valor recebido em tamanho:", validated_data.get('tamanho'))
        try:
            tamanho = Tamanho.objects.get(nome=validated_data['tamanho'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"tamanho": "Tamanho não encontrado"})
        
        # ✅ Usar first() em vez de get() para evitar múltiplas variações
        variacao = ProdutoVariacao.objects.filter(
            produto=produto,
            cor=validated_data['cor'],
            tamanho=tamanho
        ).first()
        
        if not variacao:
            variacao = ProdutoVariacao.objects.create(
                produto=produto,
                cor=validated_data['cor'],
                tamanho=tamanho,
                estoque=validated_data['estoque']
            )
        
        return variacao
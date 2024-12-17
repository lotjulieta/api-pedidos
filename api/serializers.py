from rest_framework import serializers

from app.models import (
    Company,
    Pedido,
)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'id',
            'type_request',
            'client',
            'tecnico',
            'scheme',
            'hours_worked'
        ]
        read_only_fields = ['id']


class TecnicoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    total_hours = serializers.FloatField()
    total_payment = serializers.FloatField()
    pedido_count = serializers.IntegerField()


class TecnicoInformeSerializer(serializers.Serializer):
    average_payment = serializers.FloatField()
    tecnicos_below_average = TecnicoSerializer(many=True)
    last_lowest_payment = TecnicoSerializer()
    last_highest_payment = TecnicoSerializer()

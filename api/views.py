from rest_framework import viewsets
from django.db.models import Q
from rest_framework.response import Response
from django.db.models import Sum, Count

from app.models import (
    Tecnico,
    Pedido,
    Company,
)

from app.services.tecnico_service import TecnicoPaymentService

from api.serializers import(
    CompanySerializer,
    TecnicoSerializer,
    TecnicoInformeSerializer,
    PedidoSerializer,
)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage the Company model.
    - Uses the CompanySerializer for serialization.
    - Provides basic CRUD operations for the Company model.
    """
    serializer_class = CompanySerializer
    queryset = Company.objects.filter()


class TecnicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage the Tecnico model.
    - Allows only the GET method.
    - Calculates total hours worked, number of associated orders, 
      and total payment for each technician.
    """
    http_method_names = ['get']
    serializer_class = TecnicoSerializer

    def get_queryset(self):
        queryset = Tecnico.objects.annotate(
            total_hours=Sum('pedido__hours_worked'),
            pedido_count=Count('pedido')
        ).order_by('-id')

        first_name_filter = self.request.query_params.get('first_name', None)
        last_name_filter = self.request.query_params.get('last_name', None)

        filter_conditions = Q()
        if first_name_filter:
            filter_conditions &= Q(first_name__icontains=first_name_filter)
        if last_name_filter:
            filter_conditions &= Q(last_name__icontains=last_name_filter)

        if filter_conditions:
            queryset = queryset.filter(filter_conditions)
        
        return queryset

    def list(self, request, *args, **kwargs):
        tecnicos = self.get_queryset()

        tecnico_data = []
        for tecnico in tecnicos:
            total_hours = tecnico.total_hours or 0
            payment = TecnicoPaymentService.calculate_payment(total_hours)
            tecnico_data.append({
                'id': tecnico.id,
                'full_name': tecnico.full_name,
                'total_hours': total_hours,
                'total_payment': payment,
                'pedido_count': tecnico.pedido_count
            })

        return Response(tecnico_data)


class TecnicoInformeViewSet(viewsets.ModelViewSet):
    """
    ViewSet to generate analytical reports for technicians.
    - Provides insights such as average payment, 
      technicians below the average, and details of the lowest and highest payments.
    """
    http_method_names = ['get']
    serializer_class = TecnicoInformeSerializer

    def get_queryset(self):
        return Tecnico.objects.annotate(
            total_hours=Sum('pedido__hours_worked')
        )

    def list(self, request, *args, **kwargs):
        tecnicos = self.get_queryset()

        tecnico_data = []
        total_payment = 0

        for tecnico in tecnicos:
            total_hours = tecnico.total_hours or 0
            payment = TecnicoPaymentService.calculate_payment(total_hours)
            total_payment += payment
            tecnico_data.append({
                'id': tecnico.id,
                'full_name': tecnico.full_name,
                'total_hours': total_hours,
                'total_payment': payment,
            })

        promedio_cobrado = total_payment / len(tecnicos) if tecnicos else 0

        below_average = [
            tecnico for tecnico in tecnico_data if tecnico['total_payment'] < promedio_cobrado
        ]
        last_lowest = min(tecnico_data, key=lambda x: x['total_payment'], default=None)
        last_highest = max(tecnico_data, key=lambda x: x['total_payment'], default=None)

        response_data = {
            'average_payment': promedio_cobrado,
            'tecnicos_below_average': below_average,
            'last_lowest_payment': last_lowest,
            'last_highest_payment': last_highest,
        }

        return Response(response_data)


class PedidoViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage the Pedido model.
    - Restricted to PUT, HEAD, and OPTIONS methods.
    - Provides functionality for updating orders.
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    http_method_names = ['put', 'head', 'options']

    def get_queryset(self):
        return Pedido.objects.all()

    def perform_update(self, serializer):
        serializer.save()

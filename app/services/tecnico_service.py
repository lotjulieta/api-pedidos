from django.db.models import Sum, Count
from app.models import Tecnico


class TecnicoPaymentService:
    """
    A service class that calculates payments for technicians based on their hours worked.
    The payment calculation considers different hourly rates and discounts depending on the 
    number of hours worked by the technician.
    """
    @staticmethod
    def calculate_payment(hours_worked):
        if hours_worked <= 14:
            rate = 200
            discount = 0.15
        elif 15 <= hours_worked <= 28:
            rate = 250
            discount = 0.16
        elif 29 <= hours_worked <= 47:
            rate = 300
            discount = 0.17
        else:
            rate = 350
            discount = 0.18

        gross_payment = hours_worked * rate
        net_payment = gross_payment * (1 - discount)
        return net_payment

    @staticmethod
    def get_tecnico_payments():
        tecnicos = Tecnico.objects.annotate(
            total_hours=Sum('pedido__hours_worked'),
            pedido_count=Count('pedido')
        )

        results = []
        for tecnico in tecnicos:
            total_hours = tecnico.total_hours or 0
            pedido_count = tecnico.pedido_count or 0
            payment = TecnicoPaymentService.calculate_payment(total_hours)

            results.append({
                'full_name': tecnico.full_name,
                'total_hours': total_hours,
                'total_payment': payment,
                'pedido_count': pedido_count
            })

        return results

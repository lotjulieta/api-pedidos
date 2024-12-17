import random
from django.core.management.base import BaseCommand, CommandError

from app.models import (
    Pedido,
    User,
    Tecnico,
    Scheme,
)


class Command(BaseCommand):
    """
    Django management command to generate random orders in the system.
    This command allows generating a specific number of random orders, assigning random 
    technicians, clients, and schemes for each order.

    Arguments:
        n (int): The number of orders to generate (1-100).
    """
    help = 'Comando para generar pedidos aleatorios'

    def add_arguments(self, parser):
        parser.add_argument('n', type=int, help='Número de pedidos a generar (1-100)')

    def handle(self, *args, **options):
        n = options['n']
        if n < 1 or n > 100:
            raise CommandError('N debe estar entre 1 y 100.')

        users = list(User.objects.all())
        tecnicos = list(Tecnico.objects.all())
        schemes = list(Scheme.objects.all())

        if not users:
            raise CommandError('Debe haber al menos un usuario')
        elif not tecnicos:
            raise CommandError('Debe haber al menos un técnico')
        elif not schemes:
            raise CommandError('Debe haber al menos un esquema.')

        pedidos = []
        for _ in range(n):
            pedido = Pedido(
                type_request=random.choice([Pedido.SOLICITUD, Pedido.PEDIDO]),
                client=random.choice(users),
                tecnico=random.choice(tecnicos),
                scheme=random.choice(schemes),
                hours_worked=random.randint(1, 10)
            )
            pedidos.append(pedido)

        Pedido.objects.bulk_create(pedidos)
        self.stdout.write(self.style.SUCCESS(f'{n} pedidos creados con éxito.'))

import json
from app.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from app.models import Pedido, User, Scheme, Tecnico, Company


class CompanyListCreateAPIViewTestCase(APITestCase):
    url = reverse("company-list")

    def setUp(self):
        self.username = "user_test"
        self.email = "test@rapihigar.com"
        self.password = "Rapi123"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_company(self):
        response = self.client.post(self.url,
                                    {
                                        "name": "company delete!",
                                        "phone": "123456789",
                                        "email": "test@rapihigar.com",
                                        "website": "http://www.rapitest.com"
                                    }
                                    )
        self.assertEqual(201, response.status_code)

    def test_list_company(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(json.loads(response.content)) == Company.objects.count())


class GeneratePedidosCommandTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="testuser@rapihogar.com", first_name="Test", last_name="User")
        self.scheme = Scheme.objects.create(name="Esquema Test")
        self.tecnico = Tecnico.objects.create(first_name="Tecnico", last_name="Prueba")

    def test_generate_pedidos_success(self):
        initial_count = Pedido.objects.count()
        call_command('generate_pedidos', 5)
        self.assertEqual(Pedido.objects.count(), initial_count + 5)

    def test_generate_pedidos_invalid_number(self):
        with self.assertRaises(CommandError):
            call_command('generate_pedidos', -1)
        with self.assertRaises(CommandError):
            call_command('generate_pedidos', 101)

    def test_generate_pedidos_missing_dependencies(self):
        Tecnico.objects.all().delete()
        with self.assertRaises(CommandError):
            call_command('generate_pedidos', 5)


class PedidoViewSetTestCase(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            email="cliente@test.com",
            password="password123",
            first_name="Cliente",
            last_name="Test",
            username="cliente_test"
        )
        self.scheme = Scheme.objects.create(name="Test Scheme")
        self.tecnico = Tecnico.objects.create(first_name="Tecnico", last_name="Prueba")
        self.pedido = Pedido.objects.create(
            type_request=Pedido.PEDIDO,
            client=self.client_user,
            scheme=self.scheme,
            tecnico=self.tecnico,
            hours_worked=5
        )
        self.url = reverse("pedido-detail", kwargs={"pk": self.pedido.id})
        self.client.login(email="cliente@test.com", password="password123")

    def test_update_pedido(self):
        response = self.client.put(self.url, {
            "type_request": Pedido.SOLICITUD,
            "client": self.client_user.id,
            "scheme": self.scheme.id,
            "tecnico": self.tecnico.id,
            "hours_worked": 8,
        })
        self.assertEqual(response.status_code, 200)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.hours_worked, 8)


class TecnicoViewSetTestCase(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            email="cliente@test.com",
            password="password123",
            first_name="Cliente",
            last_name="Test",
            username="cliente_test"
        )

        self.tecnico = Tecnico.objects.create(first_name="Tecnico", last_name="Test")
        self.url = reverse("tecnico-list")
        Pedido.objects.create(tecnico=self.tecnico, client=self.client_user, hours_worked=10)
        self.client.login(email="cliente@test.com", password="password123")

    def test_list_tecnicos(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["full_name"], "Tecnico Test")
        self.assertEqual(response.data[0]["total_hours"], 10)


class TecnicoInformeViewSetTestCase(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            email="cliente@test.com",
            password="password123",
            first_name="Cliente",
            last_name="Test",
            username="cliente_test"
        )

        self.url = reverse("informe-tecnico-list")

        self.tecnico1 = Tecnico.objects.create(first_name="Tecnico", last_name="One")
        self.tecnico2 = Tecnico.objects.create(first_name="Tecnico", last_name="Two")

        Pedido.objects.create(tecnico=self.tecnico1, client=self.client_user, hours_worked=10)
        Pedido.objects.create(tecnico=self.tecnico2, client=self.client_user, hours_worked=5)
        self.client.login(email="cliente@test.com", password="password123")

    def test_informe_tecnicos(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertIn("average_payment", data)
        self.assertIn("tecnicos_below_average", data)
        self.assertIn("last_lowest_payment", data)
        self.assertIn("last_highest_payment", data)

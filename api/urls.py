from rest_framework import routers
from django.urls import path, include
from .views import TecnicoViewSet, CompanyViewSet, TecnicoInformeViewSet, PedidoViewSet

router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'tecnicos', TecnicoViewSet, basename='tecnico')
router.register(r'informe-tecnicos', TecnicoInformeViewSet, basename='informe-tecnico')
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    path('', include(router.urls)),
]

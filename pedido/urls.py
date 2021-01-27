from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('pagar/<int:pk>', views.Pagar.as_view(), name="pagar"),
    path('salvarpedido', views.SalvarPedido.as_view(), name="salvarpedido"),
    path('detalhe/', views.DetalhesPedido.as_view(), name="detalhe"),
    path('lista/', views.Lista.as_view(), name="lista"),

]

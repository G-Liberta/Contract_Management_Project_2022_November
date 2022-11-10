from Contracts_api import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('contract', views.ContractViewSet)
router.register('contract_item', views.ContractItemViewSet)
router.register('hospital', views.HospitalViewSet)
router.register('warehouse', views.WarehouseViewSet)
router.register('invoice', views.InvoiceViewSet)
router.register('invoice_item', views.InvoiceItemViewSet)

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view()),
]
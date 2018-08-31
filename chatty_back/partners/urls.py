from django.urls import path
from . import views

app_name = "partners"
urlpatterns = [
    path('', views.PartnerList.as_view(), name='partner list'),
    path('main/', views.Partner_Main.as_view(), name='main partner module'),
    path('partner/', views.Partner.as_view(), name='create partner'),
    path('partner/<int:partner_id>/', views.DeletePartner.as_view(), name='delete partner'),
    path('profile/<int:partner_id>/', views.PartnerProfile.as_view(), name='get partner profile, modify partner profile'),
    path('mypartner/<int:partner_id>/', views.SetPartner.as_view(), name='set partner'),
]

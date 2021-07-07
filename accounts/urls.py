from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('create/', views.TgAccountCreateView.as_view(), name='account-create'),
    path('create/otp/<int:phone_num>', views.get_otp, name='account-otp')
]

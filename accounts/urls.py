from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('list/', views.TgAccountListView.as_view(), name='account-list'),
    path('delete/<int:pk>', views.TgAccountDeleteView.as_view(), name='account-delete'),
    path('detail/<int:pk>', views.TgAccountDetailView.as_view(), name='account-detail'),
    path('create/', views.TgAccountCreateView.as_view(), name='account-create'),
    path('create/otp/<int:phone_num>', views.get_otp, name='account-otp')
]

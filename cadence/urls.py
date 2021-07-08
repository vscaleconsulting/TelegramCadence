from django.urls import path

from . import views

app_name = 'cadence'

urlpatterns = [
    path('list/', views.CadenceListView.as_view(), name='cadence-list'),
    path('delete/<int:pk>', views.CadenceDeleteView.as_view(), name='cadence-delete'),
    path('detail/<int:pk>', views.cadence_detail, name='cadence-detail'),
    path('execute/<int:pk>', views.cadence_execute, name='cadence-execute'),
    path('create/', views.CadenceCreateView.as_view(), name='cadence-create'),
]

from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    # path('list/', views.UserListView.as_view(), name='user-list'),
    path('create/', views.UserCreateView.as_view(), name='user-create'),
    path('delete/<int:pk>', views.UserDeleteView.as_view(), name='user-delete'),
    path('login/', views.CustomLoginView.as_view(), name='user-login'),
    path('logout/', views.CustomLogoutView.as_view(), name='user-logout'),
]

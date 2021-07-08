from django.urls import path

from . import views

app_name = 'message'

urlpatterns = [
    path('<int:c_pk>/update/<int:pk>', views.MessageScriptUpdateView.as_view(), name='message-update'),
    path('<int:c_pk>/delete/<int:pk>', views.MessageScriptDeleteView.as_view(), name='message-delete')
]

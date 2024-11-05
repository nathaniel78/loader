from django.urls import path
from .views import (
    UploadView,
    UploadActionView,
    HostView, 
    HostCreateView,
    HostUpdateView,
    HostDeleteView, 
    CommandView,
    CommandCreateView,
    CommandUpdateView,
    CommandDeleteView,
)

urlpatterns = [
    path('upload/', UploadView.as_view(), name='upload'),
    path('upload/<int:host_id>/<int:command_id>/', UploadActionView.as_view(), name='uploader'),
    path('host/list/', HostView.as_view(), name='host_list'),
    path('host/form/', HostCreateView.as_view(), name='host_form'),
    path('host/update/<int:id>/', HostUpdateView.as_view(), name='host_update'),
    path('host/delete/<int:id>/', HostDeleteView.as_view(), name='host_delete'),
    path('command/list/', CommandView.as_view(), name='command_list'),
    path('command/form/', CommandCreateView.as_view(), name='command_form'),
    path('command/create/', CommandView.as_view(), name='command_create'),
    path('command/update/<int:id>/', CommandUpdateView.as_view(), name='command_update'),
    path('command/delete/<int:id>/', CommandDeleteView.as_view(), name='command_delete'),
]

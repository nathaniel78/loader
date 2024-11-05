from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/home/', permanent=True)),
    path('', include('app.urls')),  # Define o app como padrão
]

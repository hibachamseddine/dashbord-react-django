from django.contrib import admin
from django.urls import path, include
# backend/urls.py

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Vos autres URLs, comme 'admin/', 'api/', etc.
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Ajoutez ceci pour permettre à Django de servir les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

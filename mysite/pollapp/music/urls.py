from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home, name='music'),
    url(r'^convert_file', views.convert_file, name='convert_file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


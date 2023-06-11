from django.contrib import admin
from django.urls import path
from web import views
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('addData', views.putRequest),
    path('getweather', views.fetchWeather),
    path('ajax_reload_log', views.ajax_reload_log, name='ajax_reload_log'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# chandler404 = 'web.views.error_404'

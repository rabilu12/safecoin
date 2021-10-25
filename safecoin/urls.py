from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
#from main.views import IndexPageView, ChangeLanguageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('user/', include('django.contrib.auth.urls')),
    path('', include('user.urls')),
    path('members/', include("members.urls")),
    path('', include("app.urls")),

    #path('', IndexPageView.as_view(), name='index'),
    #path('i18n/', include('django.conf.urls.i18n')),
    #path('language/', ChangeLanguageView.as_view(), name='change_language'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

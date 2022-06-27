"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns # Translate en/vi
from django.utils.translation import gettext_lazy as _ # Translate en/vi


urlpatterns = [
    path(_('admin/'), admin.site.urls),
    path('rosetta/', include('rosetta.urls')),  # NEW
    path('', include('app.urls')),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns (
    path('', include('app.urls')),
    path("i18n/", include("django.conf.urls.i18n")),

    # If no prefix is given, use the default language
    prefix_default_language=False
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

 
admin.site.index_title = _('My Index Title')
admin.site.site_header = _('My Site Administration')
admin.site.site_title = _('My Site Management')
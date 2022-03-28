"""kpi URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

# from rest_framework.documentation import include_docs_urls
# from rest_framework.schemas import get_schema_view


urlpatterns = [
    path(f'{settings.ADMIN_PATH}/', admin.site.urls),
    # path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    # path('schema/', get_schema_view(title=API_TITLE)),
]

if 'visiting_management' in settings.INSTALLED_APPS:
    urlpatterns += path('', include('visiting_management.urls',
                        namespace='visiting')),

if 'template' in settings.INSTALLED_APPS:
    urlpatterns += path('', include('template.urls', namespace='template')),

if 'unical_accounts' in settings.INSTALLED_APPS:
    urlpatterns += path('', include('unical_accounts.urls',
                        namespace='unical_accounts')),

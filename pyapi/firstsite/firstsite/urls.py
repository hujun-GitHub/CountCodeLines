"""firstsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from firstsite import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [path('admin/', admin.site.urls),
    path('test_api/', views.test_api, name='test_api'),
    path('img_api/', views.img_api, name='img_api'),
    path('get_pay_img_api/', views.get_pay_img_api, name='get_pay_img_api'),
    path('is_pay_info_exist/', views.is_pay_info_exist, name='is_pay_info_exist')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
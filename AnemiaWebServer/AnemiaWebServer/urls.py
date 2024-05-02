
from django.contrib import admin
from django.urls import path
from AnemiaWebServer import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', views.test_serializers),
    path('test/<int:id>', views.test_details),
    path('postlar/', views.PostView.as_view(), name='posts_list'),
]  

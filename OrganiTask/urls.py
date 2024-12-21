from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('OrganizeMe.tasks.urls')),
    path('api/', include('OrganizeMe.notes.urls')),
    path('api/users/', include('OrganizeMe.users.urls')),
]

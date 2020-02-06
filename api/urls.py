from django.urls import path, include


urlpatterns = [
    path('projects/', include('projects.urls')),
    path('users/', include('users.urls')),
    path('groups/', include('groups.urls')),
]
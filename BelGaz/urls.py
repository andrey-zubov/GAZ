from django.contrib import admin
from django.urls import path, include
from planes.views import login_view, logout_view

from schema_graph.views import Schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path("schema/", Schema.as_view()),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('planning/', include('planes.urls')),
]

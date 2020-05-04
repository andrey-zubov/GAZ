from django.urls import path, include
from .views import (
    index,
    login_view,
    logout_view,
    planig_view,
)


urlpatterns = [
    path('', index),
    path('planing/', planig_view, name='planing')
]

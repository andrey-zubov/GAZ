from django.urls import path, include
from .views import (
    index,
    planing_finance_costs,

)


urlpatterns = [
    path('', index),
    path('plans/', planing_finance_costs, name='plans'),

]

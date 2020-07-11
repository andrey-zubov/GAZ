from django.urls import path, re_path
from . import views

app_name = "catalog"

urlpatterns = [
    path('', views.index),
    # path('01', views.catalog_funding),
    # path('02', views.catalog_activityform),
    # path('03', views.catalog_curator),
    # path('04', views.catalog_contracttype),
    # path('05', views.catalog_contractmode),
    # path('06', views.catalog_purchasetype),
    # path('07', views.catalog_stateasez),
    # path('08', views.catalog_counterpart),
    # path('09', views.catalog_contractstatus),
    # path('10', views.catalog_usertypes),
    # path('11', views.catalog_numberpztru),
    # path('12', views.catalog_currency),
    # path('13', views.catalog_report),

    re_path('^01/?(?P<param>\w+)?/$', views.catalog_funding),
    re_path('^02/?(?P<param>\w+)?/$', views.catalog_activityform),
    re_path('^03/?(?P<param>\w+)?/$', views.catalog_curator),
    re_path('^04/?(?P<param>\w+)?/$', views.catalog_contracttype),
    re_path('^05/?(?P<param>\w+)?/$', views.catalog_contractmode),
    re_path('^06/?(?P<param>\w+)?/$', views.catalog_purchasetype),
    re_path('^07/?(?P<param>\w+)?/$', views.catalog_stateasez),
    re_path('^08/?(?P<param>\w+)?/$', views.catalog_counterpart),
    re_path('^09/?(?P<param>\w+)?/$', views.catalog_contractstatus),
    re_path('^10/?(?P<param>\w+)?/$', views.catalog_usertypes),
    re_path('^11/?(?P<param>\w+)?/$', views.catalog_numberpztru),
    re_path('^12/?(?P<param>\w+)?/$', views.catalog_currency),
    path('13/', views.catalog_report),
    # Тестовая ссылка
    re_path('^(?P<catalog_id>\d+)/$', views.catalog_detail),
]

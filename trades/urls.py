from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    
    path('', views.trade_list, name='trade_list'),
    path("add/", views.add_trade, name="add_trade"),
    path('<int:trade_id>/update', views.update_trade, name='update_trade'),
    path('<int:trade_id>/delete', views.delete_trade, name='delete_trade'),
    path("analytics/", views.analytics, name="analytics"),
    #path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]

from django.contrib import admin
from django.urls import path
from botapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:telegram_id>/', views.index, name='index'),
    path('<str:telegram_id>/update_coins/', views.update_coins, name='update_coins'),
    path('<str:telegram_id>/boost/', views.boost, name='boost'),
    path('<str:telegram_id>/guid/', views.guid, name='guid'),

]

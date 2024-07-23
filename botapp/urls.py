from django.urls import path
from botapp import views

urlpatterns = [
    path('<str:telegram_id>/', views.index, name='index'),
    path('<str:telegram_id>/update_coins/', views.update_coins, name='update_coins'),
    path('<str:telegram_id>/boost/', views.boost, name='boost'),
    path('<str:telegram_id>/guid/', views.guid, name='guid'),
    path('<str:telegram_id>/friends/', views.friends, name='friends'),
    path('<str:telegram_id>/refill_limit/', views.RefillLimitView.as_view(), name='refill_limit'),

]

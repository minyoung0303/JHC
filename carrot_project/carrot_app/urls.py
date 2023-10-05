from django.urls import path
from . import views
from .views import set_region_certification, bring_to_top
from django.contrib.auth import views as auth_views


app_name = "dangun_app"

urlpatterns = [
    path("test/", views.test, name="test"),
    path("alert/<str:alert_type>", views.alert, name="alert"),
    path("", views.main, name="main"),
    path("login/", views.custom_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="dangun_app:main"), name="logout"),
    path("register/", views.register, name="register"),
    path("trade/", views.trade, name="trade"),
    path("trade_post/<int:pk>/", views.trade_post, name="trade_post"),
    path("write/", views.write, name="write"),
    path("edit/<int:id>/", views.edit, name="edit"),
    path("create_form/", views.create_post, name="create_form"),
    path("location/", views.location, name="location"),
    path("set_region/", views.set_region, name="set_region"),
    path("set_region_certification/", set_region_certification, name="set_region_certification"),
    path("search/", views.search, name="search"),
    path("chat/", views.chat_view, name="chat"),
    path("delete_post/<int:post_id>/", views.delete_post, name="delete_post"),
    path("pin_post/<int:post_id>/", bring_to_top, name="bring_to_top"),

    path('profile/', views.my_profile, name='my_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:user_id>/', views.view_profile, name='view_profile'),


    # 채팅
    path("chat_index", views.index, name='index'),  
    path('chat_index/<int:pk>/', views.chat_room, name='chat_room'),
    path('create_or_join_chat/<int:pk>/', views.create_or_join_chat, name='create_or_join_chat'),
    path('get_latest_chat/', views.get_latest_chat_no_pk, name='get_latest_chat_no_pk'),
    path('get_latest_chat/<int:pk>/', views.get_latest_chat, name='get_latest_chat'),

    path('confirm_deal/<int:post_id>/', views.ConfirmDealView.as_view(), name='confirm_deal'),

]

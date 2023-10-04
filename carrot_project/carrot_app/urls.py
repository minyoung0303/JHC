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
    path("userprofile/<str:user_id>", views.userprofile, name="userprofile"),
    path("pin_post/<int:post_id>/", bring_to_top, name="bring_to_top"),
]

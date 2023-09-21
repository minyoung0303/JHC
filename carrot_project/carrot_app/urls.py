from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


app_name = "dangun_app"
urlpatterns = [
    # 나머지 URL 패턴들을 추가
    path("login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="board_client"), name="logout"),
    path("", views.main, name="main"),
    path("search/", views.search, name="search"),
    path('register/', views.register, name='register'),
]

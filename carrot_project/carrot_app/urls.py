from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    # 나머지 URL 패턴들을 추가
    path("", LoginView.as_view(template_name="login.html"), name="login"),
]

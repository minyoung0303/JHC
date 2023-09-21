from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login


# Create your views here.
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request, "board_client")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


def main(request):
    # 데이터베이스에서 필요한 데이터 가져오기 (예: 게시물 목록)
    # posts = Post.objects.all()  # 필요한 모델에 따라 수정
    posts = {}
    # 템플릿에 데이터 전달
    context = {
        "posts": posts,
    }

    # main.html 템플릿 렌더링 및 클라이언트에 반환
    return render(request, "dangun_app/main.html", context)


def search(request):
    # query = request.GET.get('q', '')
    # posts = Post.objects.filter(title__icontains=query)
    posts = {}
    context = {
        "posts": posts,
    }
    return render(request, "dangun_app/search.html", context)


def register(request):
    return render(request, "registration/register.html")

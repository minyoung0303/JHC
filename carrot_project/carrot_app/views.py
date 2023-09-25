from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

# from .models import Post,UserProfile

from .forms import CustomLoginForm, CustomRegistrationForm  # , PostForm


# Create your views here.
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


def trade(request):
    # top_views_posts = Post.objects.filter(product_sold='N').order_by('-view_num')
    top_views_posts = {}
    # 템플릿에 데이터 전달
    return render(request, "dangun_app/trade.html", {"posts": top_views_posts})


# 중고거래상세정보(각 포스트) 화면
def trade_post(request, pk):
    # post = get_object_or_404(Post, pk=pk)

    # # 조회수 증가
    # if request.user.is_authenticated:
    #     if request.user != post.user:
    #         post.view_num += 1
    #         post.save()
    # else:
    #     post.view_num += 1
    #     post.save()

    # try:
    #     user_profile = UserProfile.objects.get(user=post.user)
    # except UserProfile.DoesNotExist:
    #         user_profile = None

    post = {}
    user_profile = {}
    context = {
        "post": post,
        "user_profile": user_profile,
    }

    return render(request, "dangun_app/trade_post.html", context)


# 거래글쓰기 화면
# @login_required
def write(request):
    # try:
    #     user_profile = UserProfile.objects.get(user=request.user)

    #     if user_profile.region_certification == 'Y':
    #         return render(request, 'dangun_app/write.html')
    #     else:
    #         return redirect('dangun_app:alert', alert_message='동네인증이 필요합니다.')
    # except UserProfile.DoesNotExist:
    return redirect("dangun_app:alert", alert_message="동네인증이 필요합니다.")


# 거래글수정 화면
def edit(request, id):
    # post = get_object_or_404(Post, id=id)
    # if post:
    #     post.description = post.description.strip()
    # if request.method == "POST":
    #     post.title = request.POST['title']
    #     post.price = request.POST['price']
    #     post.description = request.POST['description']
    #     post.location = request.POST['location']
    #     if 'images' in request.FILES:
    #         post.images = request.FILES['images']
    #     post.save()
    #     return redirect('dangun_app:trade_post', pk=id)
    post = {}
    return render(request, "dangun_app/write.html", {"post": post})


# 채팅 화면
# @login_required
def chat_view(request):
    return render(request, "dangun_app/chat.html")


# 동네인증 화면
# @login_required
def location(request):
    region = {}
    return render(request, "dangun_app/location.html", {"region": region})


# 가입 화면
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomRegistrationForm, CustomLoginForm


def register(request):
    error_message = ""
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        username = request.POST.get("username")
        if User.objects.filter(username=username).exists():
            error_message = "이미 존재하는 아이디입니다."
        elif form.is_valid():
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]

            # 비밀번호 일치 여부를 확인
            if password1 == password2:
                # 새로운 유저를 생성
                user = User.objects.create_user(username=username, password=password1)

                # 유저를 로그인 상태로 만듦
                login(request, user)

                return redirect("dangun_app:login")
            else:
                form.add_error("password2", "Passwords do not match")
    else:
        form = CustomRegistrationForm()

    return render(
        request, "registration/register.html", {"form": form, "error_message": error_message}
    )


# 로그인 화면
def custom_login(request):
    # 이미 로그인한 경우
    if request.user.is_authenticated:
        return redirect("dangun_app:main")

    else:
        form = CustomLoginForm(data=request.POST or None)
        if request.method == "POST":
            # 입력정보가 유효한 경우 각 필드 정보 가져옴
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]

                # 위 정보로 사용자 인증(authenticate사용하여 superuser로 로그인 가능)
                user = authenticate(request, username=username, password=password)

                # 로그인이 성공한 경우
                if user is not None:
                    login(request, user)  # 로그인 처리 및 세션에 사용자 정보 저장
                    return redirect("dangun_app:main")  # 리다이렉션
        return render(request, "registration/login.html", {"form": form})  # 폼을 템플릿으로 전달


# 포스트 업로드
@login_required
def create_post(request):
    # if request.method == "POST":
    #     form = PostForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         post = form.save(commit=False)  # 임시 저장
    #         post.user = request.user  # 작성자 정보 추가 (이 부분을 수정했습니다)
    #         post.save()  # 최종 저장
    #         return redirect("dangun_app:trade_post", pk=post.pk)  # 저장 후 상세 페이지로 이동
    # else:
    #     form = PostForm()
    form = {}
    return render(request, "dangun_app/trade_post.html", {"form": form})


# 포스트 검색
def search(request):
    # query = request.GET.get("search")
    # if query:
    #     results = Post.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
    # else:
    #     results = Post.objects.all()
    results = {}

    return render(request, "dangun_app/search.html", {"posts": results})


# 지역설정
@login_required
def set_region(request):
    # if request.method == "POST":
    #     #region = request.POST.get("region-setting")#

    #     if region:
    #         try:
    #             user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    #             user_profile.region = region
    #             user_profile.save()

    #             return redirect("dangun_app:location")
    #         except Exception as e:
    #             return JsonResponse({"status": "error", "message": str(e)})
    #     else:
    #         return JsonResponse({"status": "error", "message": "Region cannot be empty"})
    # else:
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)


# 지역인증 완료
@login_required
def set_region_certification(request):
    if request.method == "POST":
        request.user.profile.region_certification = "Y"
        request.user.profile.save()
        messages.success(request, "인증되었습니다")
        return redirect("dangun_app:location")

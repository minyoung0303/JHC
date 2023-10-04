from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q

from .models import Post, UserProfile

from .forms import CustomLoginForm, CustomRegistrationForm, PostForm


# 채팅테스트
# chat/views.py
from django.shortcuts import render


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


#


# 메인 화면
def main(request):
    top_views_posts = Post.objects.filter(product_sold="N").order_by("-view_num")[:4]
    return render(request, "dangun_app/main.html", {"posts": top_views_posts})


def alert(request, alert_type):
    # alert_type에 따라 다른 템플릿 선택
    if alert_type == "login":
        template_name = "dangun_app/alert_login.html"
        alert_message = "로그인해주세요!"
    elif alert_type == "region":
        template_name = "dangun_app/alert_region.html"
        alert_message = "동네인증해주세요!"
    elif alert_type == "userProfile":
        template_name = "dangun_app/alert_userProfile.html"
        alert_message = "사용자정보가 없어요!"
    else:
        # 기본 템플릿 또는 오류 처리
        template_name = "dangun_app/alert_region.html"
        alert_message = "알 수 없는 알림 유형입니다."

    context = {}  # alert_message를 컨텍스트에 추가
    return render(request, template_name)


# 테스트용 화면
def test(request):
    return render(request, "dangun_app/test.html")


# 중고거래 화면
def trade(request):
    top_views_posts = Post.objects.filter(product_sold="N").order_by("-modified_at")
    return render(request, "dangun_app/trade.html", {"posts": top_views_posts})


# 중고거래상세정보(각 포스트) 화면
def trade_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 조회수 증가
    if request.user.is_authenticated:
        if request.user != post.user:
            post.view_num += 1
            post.save()
    else:
        post.view_num += 1
        post.save()

    try:
        user_profile = UserProfile.objects.get(user=post.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    context = {
        "post": post,
        "user_profile": user_profile,
    }

    return render(request, "dangun_app/trade_post.html", context)


# 거래글쓰기 화면
@login_required
def write(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)

        if user_profile.region_certification == "Y":
            return render(request, "dangun_app/write.html")
        else:
            return redirect("dangun_app:alert", alert_type="region")
    except UserProfile.DoesNotExist:
        return redirect("dangun_app:alert", alert_type="userProfile")


# 거래글수정 화면
def edit(request, id):
    post = get_object_or_404(Post, id=id)
    if post:
        post.description = post.description.strip()
    if request.method == "POST":
        post.title = request.POST["title"]
        post.price = request.POST["price"]
        post.description = request.POST["description"]
        post.location = request.POST["location"]
        if "images" in request.FILES:
            post.images = request.FILES["images"]
        post.save()
        return redirect("dangun_app:trade_post", pk=id)

    return render(request, "dangun_app/write.html", {"post": post})


# 채팅 화면
@login_required
def chat_view(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)

        if user_profile.region_certification == "Y":
            return render(request, "dangun_app/chat.html")
        else:
            return redirect("dangun_app:alert", alert_type="region")
    except UserProfile.DoesNotExist:
        return redirect("dangun_app:alert", alert_type="userProfile")


# 동네인증 화면
@login_required
def location(request):
    try:
        user_profile = UserProfile.objects.get(user_id=request.user)
        region = user_profile.region
    except UserProfile.DoesNotExist:
        region = None

    return render(request, "dangun_app/location.html", {"region": region})


# 가입 화면
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomRegistrationForm


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
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # 임시 저장
            post.user = request.user  # 작성자 정보 추가 (이 부분을 수정했습니다)
            post.save()  # 최종 저장
            return redirect("dangun_app:trade_post", pk=post.pk)  # 저장 후 상세 페이지로 이동
    else:
        form = PostForm()
    return render(request, "dangun_app/trade_post.html", {"form": form})


# 포스트 검색
def search(request):
    query = request.GET.get("search")
    if query:
        results = Post.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
    else:
        results = Post.objects.all()

    return render(request, "dangun_app/search.html", {"posts": results})


# 지역설정
@login_required
def set_region(request):
    if request.method == "POST":
        region = request.POST.get("region-setting")

        if region:
            try:
                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.region = region
                user_profile.save()

                return redirect("dangun_app:location")
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
        else:
            return JsonResponse({"status": "error", "message": "Region cannot be empty"})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)


# 지역인증 완료
@login_required
def set_region_certification(request):
    if request.method == "POST":
        request.user.profile.region_certification = "Y"
        request.user.profile.save()
        messages.success(request, "인증되었습니다")
        return redirect("dangun_app:location")


def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        # 삭제 권한 확인
        if request.user.username == post.user.username:
            post.delete()
            # JSON 응답을 반환합니다.
            return JsonResponse({"message": "포스트가 성공적으로 삭제되었습니다."})
        else:
            # 삭제 권한이 없는 경우에 대한 처리
            return JsonResponse({"message": "삭제 권한이 없습니다."}, status=403)  # 403 Forbidden 상태 코드 반환
    except Post.DoesNotExist:
        # 포스트가 존재하지 않는 경우에 대한 처리
        return JsonResponse({"message": "포스트가 존재하지 않습니다."}, status=404)  # 404 Not Found 상태 코드 반환


# 오래된 게시글 끌어올리기 기능
from datetime import datetime, timezone


def bring_to_top(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.modified_at = datetime.now(timezone.utc)
    post.save()
    return redirect("dangun_app:trade")

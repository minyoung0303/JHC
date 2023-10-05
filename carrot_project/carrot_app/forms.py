from django import forms
from .models import Post, UserProfile
from django.forms.widgets import ClearableFileInput


class CustomLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "아이디를 입력해주세요", "class": "login-input"}),
        label="아이디",
        label_suffix="",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호를 입력해주세요", "class": "login-input"}),
        label="비밀번호",
        label_suffix="",
    )


class CustomRegistrationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "아이디를 입력해주세요", "class": "login-input"}),
        label="아이디",
        label_suffix="",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호를 입력해주세요", "class": "login-input"}),
        label="비밀번호",
        label_suffix="",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "비밀번호를 다시 입력해주세요", "class": "login-input"}
        ),
        label="비밀번호 확인",
        label_suffix="",
    )


class MultipleFileInput(ClearableFileInput):
    # 다중 파일 선택을 위해 multiple 속성 추가
    template_name = "django/forms/widgets/multiple_file_input.html"
    input_type = "file"
    needs_multipart_form = True

    def __init__(self, attrs=None):
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["attrs"]["multiple"] = True  # multiple 속성 추가
        return context


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "price", "description", "location", "images"]

    images = forms.ImageField(widget=MultipleFileInput, required=False)  # 커스텀 다중 파일 업로드 위젯 사용


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nickname", "email", "birthdate", "gender", "profile_picture"]

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


class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nickname", "email", "birthdate", "gender", "profile_picture"]

        labels = {
            "nickname": "닉네임",
            "email": "이메일",
            "birthdate": "생년월일",
            "gender": "성별",
            "profile_picture": "프로필 사진",
        }



    nickname = forms.CharField(label="닉네임", required=False)

    # 생년월일 수정 시 생일 형식 검사
    def clean_birthdate(self):
        birthdate = self.cleaned_data["birthdate"]
        return birthdate


    # 사용중인 닉네임인지 확인
    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']

        if UserProfile.objects.exclude(user=self.instance.user).filter(nickname=nickname).exists():
            raise forms.ValidationError('이미 사용 중인 닉네임입니다.')
        
        return nickname

    clear_profile_picture = forms.BooleanField(
        required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    def save(self, commit=True):
        instance = super(UserProfileForm, self).save(commit=False)

        if self.cleaned_data.get('clear_profile_picture'):
            instance.profile_picture.delete(save=False)
            instance.profile_picture = "profile_pictures/default_profile_picture.png"

        if commit:
            instance.save()
        return instance
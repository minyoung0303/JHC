from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Image(models.Model):
    image = models.ImageField(upload_to="post_images/")


class Post(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    location = models.CharField(max_length=100)
    images = models.ManyToManyField(Image)  # 다중 이미지 관계 설정
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, to_field="username")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True)

    product_reserved = models.CharField(max_length=1, default="N")  # 예약 여부
    product_sold = models.CharField(max_length=1, default="N")  # 판매 여부

    view_num = models.PositiveIntegerField(default=0)  # 조회 수
    chat_num = models.PositiveIntegerField(default=0)  # 채팅 수

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    birthdate = models.DateField(null=True)
    gender = models.CharField(
        max_length=1, choices=[("M", "Male"), ("F", "Female"), ("O", "Other")], null=True
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", default="profile_pictures/default_profile_picture.png"  # 기본 프로필 사진 경로
    )
    region = models.CharField(max_length=100, null=True)
    region_certification = models.CharField(max_length=1, default="N")


    def __str__(self):
        return f"{self.user.username} Profile"


class MannerTemperature(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="manner_temperature"
    )
    total_votes = models.PositiveIntegerField(default=1)  # 전체 투표 수
    total_score = models.PositiveIntegerField(default=30)  # 전체 점수 합

    def average_temperature(self):
        if self.total_votes > 0:
            return self.total_score / self.total_votes
        else:
            return 0

    def update_temperature(self, score):
        self.total_votes += 1
        self.total_score += score
        self.save()


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

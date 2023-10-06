import boto3
import os, json
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# S3와 연결하는 배경 코드 블럭
BASE_DIR = Path(__file__).resolve().parent

secret_file = os.path.join(BASE_DIR, "secrets.json")  # secrets.json 파일 위치를 명시

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

AWS_REGION = "ap-northeast-2"
AWS_STORAGE_BUCKET_NAME = get_secret("BUCKET_NAME")
AWS_ACCESS_KEY_ID = get_secret("ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = get_secret("SECRET_ACCESS_KEY")

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


# 생성할 디렉토리 이름
# new_directory_name = "profile_pictures"

# def create_s3_directory(bucket_name, directory_name):
#     try:
#         s3_client.put_object(Bucket=bucket_name, Key=f"{directory_name}/")
#         print(f"루트 경로에 새로운 디렉토리를 생성했습니다.: {directory_name}")
#     except Exception as e:
#         print(f"에러 발생: {e}")


# 저장할 이미지의 경로(로컬 환경 주소)
image_file_path = "C:\\Users\\hoola\\Desktop\\proj\\JHC\\JHC\\carrot_project\\carrot_app\\static\\profile_pictures\\default_profile_picture.png"
image_diretory_path = "profile_pictures"

def upload_image_to_s3(bucket_name, directory_name, image_file_path):
    try:
        image_name = os.path.basename(image_file_path)
        s3_key = f"{directory_name}/{image_name}"

        s3_client.upload_file(
            image_file_path,
            bucket_name,
            s3_key,
            ExtraArgs={
                'ContentType': 'image/png',  # PNG 이미지의 콘텐츠 타입 설정
                'ContentDisposition': 'inline'  # Content-Disposition을 inline으로 설정
            }
            
            )
        
        print(f"S3에 이미지 업로드 완료: {s3_key} ")
    except Exception as e:
        print(f"에러 발생: {e}")

# 삭제할 이미지의 경로
# image_key = "profile_pictures/default_profile_picture.png"


# 새 디렉토리 생성
# create_s3_directory(AWS_STORAGE_BUCKET_NAME, new_directory_name)

# 이미지를 디렉토리에 업로드
upload_image_to_s3(AWS_STORAGE_BUCKET_NAME, image_diretory_path, image_file_path)

# 이미지 삭제
# try:
#     s3_client.delete_object(
#         Bucket=AWS_STORAGE_BUCKET_NAME,
#         Key=image_key
#     )
#     print(f"이미지 {image_key}가 정삭적으로 삭제되었습니다.")
# except Exception as e:
#     print(f"이미지 삭제 오류 발생 {e}")
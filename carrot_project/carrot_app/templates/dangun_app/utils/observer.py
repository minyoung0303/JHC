import boto3
from pathlib import Path
import os, json
from django.core.exceptions import ImproperlyConfigured


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


# AWS S3 설정
AWS_REGION = "ap-northeast-2"
AWS_STORAGE_BUCKET_NAME = get_secret("BUCKET_NAME")
AWS_ACCESS_KEY_ID = get_secret("ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = get_secret("SECRET_ACCESS_KEY")

# S3 클라이언트 생성
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# 버킷 내의 디렉토리 구조 확인
def list_s3_directory_contents(bucket_name, prefix):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        contents = response.get('Contents', [])

        for item in contents:
            # 파일 키와 파일 크기 출력
            file_key = item['Key']
            file_size = item['Size']
            print(f"File: {file_key}, Size: {file_size} bytes")

    except Exception as e:
        print(f"An error occurred: {e}")

# 원하는 디렉토리 구조 및 파일 목록 조회
list_s3_directory_contents(AWS_STORAGE_BUCKET_NAME, '')
from fabric.contrib.files import append, exists, sed, put
from fabric.api import env, local, run, sudo
import random
import os
import json

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
print("settings.py의 코드 폴더 : ", PROJECT_DIR)
#C:\Users\박준호\AppData\Local\Programs\Python\Python36\Lib\site-packages\django\bin\ch3\mysite


BASE_DIR = os.path.dirname(PROJECT_DIR)

print("manage.py의 코드 폴더 : ",BASE_DIR)
#print("manage.py의 실제 폴더 : C:\Users\박준호\AppData\Local\Programs\Python\Python36\Lib\site-packages\django\bin\ch3\ ")

# deploy.json파일을 불러와 envs변수에 저장합니다.
with open(os.path.join(PROJECT_DIR, "deploy.json")) as f:
    envs = json.loads(f.read())

REPO_URL = envs['REPO_URL']
PROJECT_NAME = envs['PROJECT_NAME']
REMOTE_HOST_SSH = envs['REMOTE_HOST_SSH']
REMOTE_HOST = envs['REMOTE_HOST']
REMOTE_USER = envs['REMOTE_USER']
REMOTE_PASSWORD = envs['REMOTE_PASSWORD']
# 아래 부분은 Django의 settings.py에서 지정한 STATIC_ROOT 폴더 이름, STATID_URL, MEDIA_ROOT 폴더 이름을 입력해주시면 됩니다.
STATIC_ROOT_NAME = '/polls/'
STATIC_URL_NAME = '/polls/static/'
MEDIA_ROOT = 'uploads'


# Fabric이 사용하는 env에 값들을 저장합니다.
env.user = REMOTE_USER
username = env.user
env.hosts = [
    REMOTE_HOST_SSH, # 리스트로 만들어야 합니다.
    ]
env.password = REMOTE_PASSWORD
# 원격 서버에서 장고 프로젝트가 있는 위치를 정해줍니다.
project_folder = '/home/{}/{}'.format(env.user, PROJECT_NAME)


# APT로 설치할 목록을 정해줍니다.
apt_requirements = [
    'ufw', # 방화벽
    'curl',
    'git', # 깃
    'python3-dev', # Python 의존성
    'python3-pip', # PIP
    'build-essential', # C컴파일 패키지
    'python3-setuptools', # PIP
    'apache2', # 웹서버 Apache2
    'libapache2-mod-wsgi-py3', # 웹서버~Python3 연결
    # 'libmysqlclient-dev', # MySql
    'libssl-dev', # SSL
    'libxml2-dev', # XML
    'libjpeg8-dev', # Pillow 의존성 패키지(ImageField)
    'zlib1g-dev', # Pillow 의존성 패키지
]
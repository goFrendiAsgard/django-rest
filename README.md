#jApa ini

Percobaan membuat aplikasi Django dengan [django-rest-framework](https://www.django-rest-framework.org/)

# Tujuan

- Membuat aplikasi Django dengan beberapa fitur:
    - [REST API](https://en.wikipedia.org/wiki/Overview_of_RESTful_API_Description_Languages)
    - Autentikasi menggunakan [JWT](https://en.wikipedia.org/wiki/JSON_Web_Token)

Dengan menyediakan API endpoint, kita bisa lebih agnostik dalam hal tampilan. Kita bisa menggunakan API endpoints yang sama untuk aplikasi web/mobile/desktop. Artinya kita cukup menulis satu business logic untuk tampilan-tampilan yang kelak akan kita buat. Ini akan membuat aplikasi backend kita menjadi lebih maintainable.

Untuk autentikasi, ada beberapa proses autentikasi yang umum dipakai:

- Basic auth:
    Kita perlu mengirimkan user dan password sebagai HTTP header. Cara ini kurang aman, dan biasanya tidak diterapkan di level production karena password perlu dikirimkan berkali-kali dalam bentuk plain-text.

- COOKIE based:

    Keseluruhan informasi disimpan di COOKIE. Selanjutnya COOKIE akan dikirimkan setiap kali melakukan request ke user. Hal ini kurang aman juga, karena COOKIE disimpan di sisi client dan mudah di temper (diubah isinya).

- SESSION based:

    Secara low level, cara ini menggunakan mekanisme yang mirip seperti COOKIE, hanya saja data autentikasinya disimpan di server (dalam bentuk file ataupun disimpan dalam database). COOKIE hanya akan menyimpan session id saja, sehingga data-data autentikasi tidak ada di client. Cara ini cukup umum dipakai dan relatif lebih aman.

- Token based:

    Data autentikasi diubah ke dalam bentuk token dan dikirim setiap kali client melakukan request ke server. Cara ini membebaskan server dari tanggung jawab untuk menyimpan session. Server hanya perlu bisa memetakan token menjadi informasi. Cara ini cukup aman selama ada cara menjamin bahwa data yang ada di token tidak bisa di-temper (diubah). Misalnya dengan menggunakan hash.
    
    Kelemahan dari token based authentication adalah server harus memiliki satu cara untuk menonaktifkan token. Kita bisa menggunakan mekanisme "expired" untuk ini. Sehingga biasanya kita perlu memperbaharui token setiap beberapa saat sebelum expired.

Kita akan menggunakan salah satu token based authentication yang cukup populer, yakni JWT (JSON Web Token).

Dengan menggunakan JWT, kita tidak perlu memiliki media penyimpanan khusus untuk menyimpan informasi user yang login.


# Yang diperlukan

- [Python](https://www.python.org/) dan [pip](https://pypi.org/project/pip/)
- API platform. Bisa menggunakan salah satu dari:
    - [Postman](https://www.postman.com/) (paling banyak fiturnya)
    - [insomnia](https://insomnia.rest/) (mirp seperti postman)
    - [curl](https://curl.se/) (berjalan di CLI)
- Git client

# Menjalankan repo ini

Untuk menjalankan aplikasi ini secara cepat, kita bisa menjalankan:

```bash
# pindah ke folder myproject
cd myproject
# lakukan migrasi
python manage.py migrate
# jalankan aplikasi
python manage.py runserver
```


# Tahapan membuat aplikasi dari awal

Di sini kita akan melihat langkah pembuatan aplikasi dari awal.

Kalian bisa mengikuti semua tahapan yang ada di repository yang baru.

Nantinya kita akan melakukan beberapa tahapan kerja mulai dari menginstall `django`, melakukan pembuatan `view` dan `model`, sampai ke uji coba aplikasi.


## Install venv

Langkah paling awal yang sangat disarankan saat kita memulai sebuah proyek Python adalah membuat virtual environment (venv). Venv memungkinkan kita untuk memiliki kumpulan pip packages yang terpisah untuk masing-masing project.

```bash
python -m venv venv
```

## Inisialisasi git

Git adalah vesion control yang sangat populer.

Kita bisa membuat repositori git secara gratis di [GitHub](https://github.com).

Di sisi client, yang perlu kita lakukan adalah menginisiasi project dan menghubungkannya ke remote server:

```bash
# Inisiasi git repository (hanya dilakukan sekali di awal)
git init 

# set remote dengan nama "origin"
git remote add origin git@github.com:User/UserRepo.git

# lakukan perubahan seperlunya, dan simpan perubahan ke staging
git add . -A

# Commit perubahan
git commit -m 'first commit'

# Push perubahan ke server
git push -u origin master
```

Lebih lanjut tentang git, silahkan ikuti [tutorial ini](https://www.w3schools.com/git/default.asp).

## Install pip packages yang diperlukan

```bash
source venv/bin/activate
pip install django djangorestframework PyJWT
```

Supaya ke depannya kita mendapatkan versi package yang sesuai dengan kode yang kita buat, kita bisa menjalankan:

```bash
pip freeze
```

Kita akan memperoleh tampilan seperti ini:

```
asgiref==3.6.0
Django==4.1.5
djangorestframework==3.14.0
PyJWT==2.6.0
pytz==2022.7
sqlparse==0.4.3
```

Yang kita perlukan hanyalah `Django` dan `djangorestframework`. Package-package yang lain merupakan dependency dari kedua package tersebut, sehingga kita tidak perlu memastikan exact version nya.

Dari output yang sudah kita dapatkan, kita perlu membuat sebuah file dengan nama `requirements.txt` dengan isi sebagai berikut:

```
Django==4.1.5
djangorestframework==3.14.0
PyJWT==2.6.0
```

File `requirements.txt` perlu kita update setiap kali kita menginstall package baru.

Untuk menginstall package-package yang terdapat dalam file `requirements.txt` kita bisa menjalankan:

```bash
pip install -r requirements.txt
```

## Scaffold proyek

Django menyediakan perintah untuk membuat sebuah proyek.

```bash
django-admin startproject myproject
```

Kita bisa melihat bahwa dalam folder `myproject` terdapat:

- directory `myproject` yang berisi konfigurasi proyek kita
- file `manage.py` yang berfungsi untuk membantu kita memanage proyek yang sudah kita buat.

Lakukan perintah berikut untuk mengetahui kapabilitas dari file `manage.py`:

```bash
cd myproject
python manage.py
```

## Scaffold aplikasi

Dalam sebuah proyek, bisa terdapat beberapa aplikasi.

Biasanya satu aplikasi terdiri dari kode-kode yang secara use-case berdekatan/saling terkait. Misalnya ada domain penjualan, domain pembelian, dsb.

Kita akan membuat dua buah aplikasi:

- `accounts` untuk mengurus autentikasi
- `notes` untuk membuat catatan

Pastikan kita sudah ada di dalam direktori `myproject`. Setelah itu, jalankan perintah berikut:

```bash
python manage.py startapp accounts
python manage.py startapp notes
```

Usai menjalankan perintah di atas, kita akan mendapatkan dua directory baru di dalam directory `myproject`:

- `accounts`
- `notes`

## Mengubah setting proyek

Untuk menghubungkan aplikasi yang sudah ke buat ke dalam myproject, maka kita bisa menambahkan beberapa bagian di `myproject/settings.py`.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # tambahkan bagian ini
    'accounts', # tambahkan bagian ini
    'notes', # tambahkan bagian ini
]

# kode konfigurasi yang lain

AUTH_USER_MODEL = 'accounts.User' # tambahkan ini
JWT_SECRET = 'rahasia' # tambahkan ini
APPEND_SLASH = False # tambahkan ini
```

Selain menambahkan app accounts dan notes ke dalam myproject, kita juga perlu mendefinisikan beberapa hal:

- `AUTH_USER_MODEL`: Menyatakan model yang akan kita pakai untuk autentikasi. Model ini akan kita buat pada langkah berikutnya
- `JWT_SECRET`: Salt yang akan dipakai untuk hashing JWT token
- `APPEND_SLASH`: Setting untuk tidak menambahkan `/` di akhir url.

## Membuat model untuk aplikasi accounts

Pertama-tama kita perlu membuat model untuk aplikasi accounts (`myproject/accounts/models.py`):

```python
from typing import Any, Optional, Mapping
from django.db import models
from django.contrib.auth import models as auth_models
from django.conf import settings

import jwt
import datetime

class User(auth_models.AbstractUser):

    def to_dict(self) -> Mapping[str, Any]:
        return {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }


class UserService():

    def get_user(self, email: str) -> User:
        user = User.objects.filter(email=email).first()
        return user 


    def create_user(self, username: str, first_name: str, last_name: str, email: str, password: Optional[str] = None) -> User:
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        if password is not None:
            user.set_password(password)
        user.save()
        return user
    

    def create_token(self, user_id:int) -> str:
        payload = dict(
            id=user_id,
            exp=datetime.datetime.utcnow() + datetime.timedelta(hours=24), #delais d'expiration
            iat=datetime.datetime.utcnow()
        )
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
        return token
```

Dalam kode model kita, terdapat dua class. yakni `User` dan `UserService`.

`User` merupakan turunan dari `auth_models.AbstractUser` yang merupakan class bawaan `django-rest-framework`.
Satu hal yang perlu kita tambahkan di sini adalah method `to_dict`. Kegunaannya adalah untuk mengubah object user ke dalam bentuk dictionary sehingga bisa di parse oleh Django sebagai response.

`UserService` merupakan abstraksi untuk me-manage user sesuai dengan use-case:

- mendapatkan user berdasarkan email
- membuat user baru
- membuat token untuk user

## Membuat authentication class

Kita perlu mendapatkan informasi user berdasarkan token yang dikirimkan oleh client.

Nantinya token yang dimiliki client akan berasal dari `UserService.create_token`. Token ini akan berisi informasi `user_id`

Authentication class yang kita buat perlu mengekstrak informasi `user_id` ini untuk mendapatkan object user yang relevan.

Letakkan kode berikut di myproject/accounts/authentication.py:

```python
from django.conf import settings
from rest_framework import authentication, exceptions
import jwt

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get('jwt')
        print(token)
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        except:
            raise exceptions.AuthenticationFailed('Unauthorized')
        user = User.objects.filter(id=payload['id']).first()
        print(user)
        return (user, None)
```


## Membuat dan menjalankan migrasi

Setelah selesai membuat model, kita bisa mencoba untuk membuat dan menjalankan migrasi berdasarkan model yang baru saja kita buat:

```bash
python manage.py makemigration
python manage.py migrate
```

## Membuat view dan URL

Dengan django rest framework, kita bisa membuat class-based view untuk menangani HTTP request dengan method tertentu.

Caranya, kita hanya perlu membuat method sesuai dengan HTTP method yang ingin kita sediakan (misal post/get/put/delete).

Kita juga bisa menambahkan `authentication_classes` dan `permission_classes` untuk autentikasi.

Letakkan kode berikut di `myproject/accounts/view.py`:

```python
from django.shortcuts import render
from rest_framework import views, response, exceptions, permissions

from .models import UserService, User
from .authentication import JWTAuthentication

user_service = UserService()

class RegisterApi(views.APIView):
    
    def post(self, request):
        user = user_service.create_user(
            username=request.data['username'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            email=request.data['email'],
            password=request.data['password'] if 'password' in request.data else None
        )
        return response.Response(data=user.to_dict())


class LoginApi(views.APIView):
    def post(self, request):
        email=request.data['email']
        password=request.data['password']
        user = user_service.get_user(email)
        if user is None or not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed('Invalid Credentials')
        token = user_service.create_token(user_id=user.id)
        resp = response.Response(data={'token': token})
        resp.set_cookie(key="jwt", value=token, httponly=True)
        return resp 


class UserApi(views.APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        user = request.user
        return response.Response(user.to_dict())


class LogoutApi(views.APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        resp = response.Response()
        resp.delete_cookie('jwt')
        resp.data = {'message': 'so long farewell'}
        return resp
```

Usai membuat view, kita perlu membuat url patterns yang mengarah ke view kita. Letakkan kode berikut di `myproject/accounts/urls.py`:

```python
from django.urls import path
from .views import RegisterApi, LoginApi, UserApi, LogoutApi

urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
    path('login/', LoginApi.as_view(), name='login'),
    path('me/', UserApi.as_view(), name='me'),
    path('logout/', LogoutApi.as_view(), name='logout'),
]
```


## Registrasi URL

Langkah terakhir yang perlu kita lakukan adalah meregistrasikan url patterns di aplikasi `accounts` ke `myproject`

Caranya, kita cukup menambahkan kode berikut ke file `myproject/myproject/urls.py`:

```py
from django.urls import path, include # tambahkan ini

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')), # tambahkan ini
]
```

## Aplikasi notes

Setelah membuat kode-kode aplikasi untuk autentikasi, berikutnya kita perlu membuat kode-kode aplikasi untuk use-case utama kita, yakni insert/update/delete catatan.

File-file yang perlu dibuat adalah sebagai berikut.

`myproject/notes/models.py`

```python
from typing import Any, Mapping
from django.db import models

class Note(models.Model):
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]


    def to_dict(self) -> Mapping[str, Any]:
        return {
            'body': self.body,
            'updated': self.updated,
            'created': self.created,
        }


    class Meta:
        ordering = ['-updated']
```

`myproject/notes/views.py`

```
from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import permissions


from .models import Note
from accounts.authentication import JWTAuthentication


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def notes(request):
    if request.method == 'POST':
        return create_note(request)
    if request.method == 'GET':
        return get_notes(request)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def notes_pk(request, pk):
    if request.method == 'GET':
        return get_note(request, pk)
    if request.method == 'PUT':
        return update_note(request, pk)
    if request.method == 'DELETE':
        return delete_note(request, pk)


def get_notes(request):
    notes = Note.objects.all()
    return Response([note.to_dict() for note in notes])


def get_note(request, pk):
    note = Note.objects.get(id=pk)
    return Response(note.to_dict())


def create_note(request):
    note = Note.objects.create(
        body=request.data['body']
    )
    return Response(note.to_dict())


def update_note(request, pk):
    note = Note.objects.get(id=pk)
    note.body = request.data['body']
    note.save()
    return Response(note.to_dict())


def delete_note(request, pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return Response(note.to_dict())
```

`myproject/notes/urls.py`

```python
from django.urls import path
from .views import notes_pk, notes

urlpatterns = [
    path('notes/<str:pk>/', notes_pk),
    path('notes/', notes),
]
```

Dan terakhir, kita perlu menambahkan url pattern kita ke `myproject/myproject/urls.py`:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('', include('notes.urls'))
]
```

Setelah semuanya siap, kita bisa membuat dan menjalankan migrasi:

```bash
python manage.py makemigration
python manage.py migrate
```

# Uji coba

Sekarang waktunya kita mencoba menjalankan `myproject`

```bash
python manage.py runserver
```

Kita bisa mulai dengan mengirimkan beberapa request menggunakan CURL/postman/insomnia

## Register

```
curl --location --request POST 'http://localhost:8000/account/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "anton",
    "first_name": "anton",
    "last_name": "antonio",
    "email": "antonio@gmail.com",
    "password": "anton"
}'
```

## Login

```
curl --location --request POST 'http://localhost:8000/account/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "antono@gmail.com",
    "password": "anton"
}'
```

Setelah login, kita akan mendapatkan token berikut:

```
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNjczMzk3MjE3LCJpYXQiOjE2NzMzMTA4MTd9.HLNWn8t5X-tv5Crm7Vim6-HMb6nV-56RxWVuqHavbWQ"
}
```

Token ini perlu kita sertakan dalam request-request selanjutnya.


## Create notes

```
curl --location --request POST 'http://localhost:8000/notes/' \
--header 'Content-Type: application/json' \
--header 'Cookie: jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNjczMzk3MTIzLCJpYXQiOjE2NzMzMTA3MjN9.c2ZOBkS-5pwvmI-RYMwuT70eU4rrMjDBh0bmDitWONk' \
--data-raw '{
    "body": "lorem ipsum dolor sit amet"
}'
```

## Get notes

```
curl --location --request GET 'http://localhost:8000/notes/' \
--header 'Cookie: jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiZXhwIjoxNjczMzk3MTIzLCJpYXQiOjE2NzMzMTA3MjN9.c2ZOBkS-5pwvmI-RYMwuT70eU4rrMjDBh0bmDitWONk'
```

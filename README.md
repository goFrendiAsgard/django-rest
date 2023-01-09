# Apa ini

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

## Membuat model untuk aplikasi accounts

## Menjalankan migrasi

## Membuat view dan URL

## Registrasi view dan URL


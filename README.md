
# Backend dengan FastAPI dan python-JOSE (JWT)

Backend dengan framework FastAPI, menggunakan database mysql.
Authentifikasi menggunakan python-JOSE[cryptography] (JWT)


Aktfikan venv : .\pro1\Scripts\Activate.ps1

Running uvicorn : uvicorn main:app --reload

Akses web : 127.0.0.1:8000

Akses fungsi API : 127.0.0.1:8000/docs

Package install :

pip install fastapi uvicorn pymysql sqlalchemy "python-jose[cryptography]" "passlib[bcrypt]" python-multipart




## Usage/Examples

Untuk customer melihat produk dari web

127.0.0.1:8000/produk 


Untuk fungsi api dan pengetesan api lengkap bisa langsung ke :

127.0.0.1:8000/docs

Konfigurasi database diatur di file : database.py

Database awal tidak ada tabelnya, jalankan fungsi api create merch /auth/merchant/daftar untuk menambah akun merchant dan tabel smuanya akan tersedia. 

Untuk menambah produk di bagian fungsi api /merchant/buatproduk/

Untuk fungsi lainnya bisa dilihat di 127.0.0.1:8000/docs (tidak perlu postman untuk pengujian api)


Untuk customer tidak menggunakan sistem login / authentifikasi, jadi customer langsung belanja dengan menggunakan id barang dan jumlah, subtotal secara otomatis dihitung dan akan menampilkan diskon dan bebas ongkir. Dengan ketentuan setiap total transaksi produk diatas 15000 akan mendapatkan bebas ongkir, dan jika total transaksi produk diatas 50000 mendapatkan diskon sebesar 10%. Jumlah diskon dan ongkir (free /tidak) akan direspon lewat json.
Semua belanja custumer akan disimpan di tabel penjualan.

Sistem token / login digunakan untuk kegiatan merchant, seperti menambah produk, menghapus produk dan melihat penjualan. Kegiatan login bisa dilakukan dengan menu gembok di fungsi api diwebsite. 







## Authors

- [@rahulakita](https://github.com/rahulakita)


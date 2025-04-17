# PM25_Monthly
Calculating monthly PM 2.5 values in Indonesia at district level using average weighted area.

Ekstraksi dan interpolasi menggunakan metode IDW untuk menghitung nilai PM 2.5.
Repository ini melakukan perhitungan area weighted average dan interpolasi IDW untuk PM 2.5 setiap bulan di Indonesia pada level kabupaten dari file NetCDF.

## 🔧 Requirements
- Python >= 3.8
- Lihat `requirements.txt`

## 🚀 Cara Menjalankan Kode

Run file `Run_all.ipynb` di Github Codespaces

## Note
Terdapat keterbatasan pemrosesan di Codespaces Github untuk file `Run.ipynb` karena Google Drive memiliki limit akses. Kode Bisa dijalankan di Google Colab atau agar lebih aman bisa dijalankan di komputer lokal, hanya mengganti Path file (di bagian bawah) ke directory penyimpanan file NetCDF dan Shapefile batas administrasi.

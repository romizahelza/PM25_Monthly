# PM25_Monthly
Calculating monthly PM 2.5 values in Indonesia at district level using average weighted area.

Ekstraksi dan interpolasi menggunakan metode IDW untuk menghitung nilai PM 2.5.
Repository ini melakukan perhitungan area weighted average dan interpolasi IDW untuk PM 2.5 setiap bulan di Indonesia pada level kabupaten dari file NetCDF.

## 🔧 Requirements
- Python >= 3.8
- Lihat `requirements.txt`

## 📁 Struktur Folder Repository
- `Data/PM2.5/` → Tempatkan file `.nc` PM2.5 di sini.
- `Data/RBI_Indonesia` → shapefile administrasi Indonesia level kabupaten/kota
- `Hasil` → Folder hasil

## 🚀 Cara Menjalankan Kode

```bash
pip install -r requirements.txt
python PM25_IDW.py

# 📈 Dashboard Analisis & Prediksi Penjualan

Dashboard interaktif menggunakan **Streamlit** untuk menganalisis data penjualan dan melakukan prediksi ke depan berdasarkan data historis.

## 🚀 Fitur Utama

- 📊 Ringkasan penjualan total dan harian
- 📈 Visualisasi penjualan harian dan per kategori
- 🔍 Dekomposisi tren, musiman, dan residual dengan time series
- 🤖 Prediksi penjualan 7 hari ke depan menggunakan:
  - Simple Exponential Smoothing (SES)
  - Holt-Winters (additive)
- ⬇️ Download hasil forecast dalam format CSV
- 📤 Upload data baru (file CSV)

## 🗂️ Struktur File

```
dashboard-penjualan/
├── app.py                  # Aplikasi utama Streamlit
├── penjualan.csv           # Data penjualan contoh (opsional)
├── requirements.txt        # Dependensi untuk deployment
└── README.md               # Dokumen ini
```

## 📌 Format Data Penjualan

File CSV harus memiliki kolom berikut:

| Kolom     | Tipe Data   | Contoh           |
|-----------|-------------|------------------|
| tanggal   | datetime    | 2025-04-01        |
| produk    | string      | Produk A          |
| kategori  | string      | Kategori 1        |
| total     | float/int   | 125000            |

## 💻 Cara Menjalankan Lokal

1. Clone repo ini:
    ```bash
    git clone https://github.com/username/dashboard-penjualan.git
    cd dashboard-penjualan
    ```

2. Install dependensi:
    ```bash
    pip install -r requirements.txt
    ```

3. Jalankan Streamlit:
    ```bash
    streamlit run app.py
    ```

## ☁️ Deploy ke Streamlit Cloud

1. Upload semua file ke GitHub
2. Buka [streamlit.io/cloud](https://streamlit.io/cloud)
3. Klik **“New App”**, pilih repo ini
4. Pilih file `app.py` lalu klik **Deploy**

---

🧑‍💻 Dibuat oleh: Andy Sarbini 
📬 Kontak: kangandy09@gmail.com

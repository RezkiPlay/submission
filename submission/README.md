# 🚲 Bike Sharing Data Analysis Project

Proyek analisis data menggunakan **Capital Bikeshare Washington D.C. Dataset (2011–2012)**.

## 📁 Struktur Direktori

```
submission/
├── dashboard/
│   ├── main_data.csv       # Data harian (cleaned)
│   ├── hour_data.csv       # Data per jam (cleaned)
│   └── dashboard.py        # Streamlit dashboard
├── data/
│   ├── day.csv             # Data mentah harian
│   ├── hour.csv            # Data mentah per jam
│   └── Readme.txt          # Dokumentasi dataset asli
├── notebook.ipynb          # Jupyter Notebook analisis lengkap
├── requirements.txt        # Daftar library Python
└── README.md               # Panduan ini
```

## 📊 Pertanyaan Bisnis

1. **Pola Per Jam:** Bagaimana pola rata-rata penyewaan sepeda per jam antara hari kerja dan hari libur/akhir pekan, dan pada jam berapa permintaan mencapai puncaknya?

2. **Faktor Lingkungan:** Faktor lingkungan apa (musim, kondisi cuaca, suhu) yang paling berpengaruh terhadap jumlah penyewaan sepeda harian?

## 🚀 Cara Menjalankan Dashboard

### Prasyarat

Pastikan Python 3.9+ sudah terinstall.

### Langkah-langkah

1. **Clone / Ekstrak** folder `submission` ke direktori lokal Anda.

2. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Masuk ke folder dashboard:**
   ```bash
   cd submission/dashboard
   ```

4. **Jalankan Streamlit:**
   ```bash
   streamlit run dashboard.py
   ```

5. **Buka browser** dan akses: `http://localhost:8501`

### Catatan

- File `main_data.csv` dan `hour_data.csv` **harus berada di folder yang sama** dengan `dashboard.py` saat menjalankan perintah `streamlit run`.
- Dashboard memiliki **sidebar filter** untuk memilih tahun, musim, dan rentang tanggal.

## 📦 Library yang Digunakan

| Library | Kegunaan |
|---------|----------|
| `pandas` | Manipulasi dan analisis data |
| `numpy` | Komputasi numerik |
| `matplotlib` | Visualisasi data |
| `seaborn` | Visualisasi statistik |
| `streamlit` | Pembuatan dashboard interaktif |

## 🔗 Sumber Dataset

- **Dataset:** [Bike Sharing Dataset – Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)
- **Sumber asli:** Capital Bikeshare, Washington D.C. | [capitalbikeshare.com](http://capitalbikeshare.com/system-data)
- **Referensi:** Fanaee-T, H. & Gama, J. (2013). *Event labeling combining ensemble detectors and background knowledge*. Progress in Artificial Intelligence, Springer.

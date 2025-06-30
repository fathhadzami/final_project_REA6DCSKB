# 💸 PatunganApp

Aplikasi web untuk membagi tagihan belanja dengan teman-teman secara otomatis. Upload foto struk/bill, tambahkan teman, dan bagi tagihan dengan mudah!

## ✨ Fitur

- 📷 **Upload Struk**: Upload foto struk belanja (JPG, PNG)
- 🤖 **AI Recognition**: Ekstraksi data struk otomatis menggunakan AI
- ✏️ **Edit Data**: Edit dan tambah item struk secara manual
- 👥 **Kelola Teman**: Tambah daftar teman yang ikut patungan
- 💰 **Metode Pembagian**:
  - Bagi rata untuk semua
  - Berdasarkan item yang dibeli
- 📊 **Hasil Detail**: Laporan lengkap siapa bayar berapa

## 🛠️ Teknologi

- **Python 3.8+**
- **Streamlit** - Framework web app
- **Streamlit Router** - Routing management
- **PIL (Pillow)** - Image processing
- **Pandas** - Data manipulation
- **OpenRouter API** - AI image recognition
- **Claude 3.5 Sonnet** - AI model untuk OCR

## 📦 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/fathhadzami/final_project_REA6DCSKB.git
cd final_project_REA6DCSKB
```

### 2.  Buat virtual environment (direkomendasikan)
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Di Windows, gunakan `venv\Scripts\activate`
    ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Buat file `.env` atau bisa copy dari file `.env.example` di root directory:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_API_BASE=https://openrouter.ai/api/v1/chat/completions
AI_MODEL="anthropic/claude-3.5-sonnet"
```

### 5. Dapatkan API Key
1. Daftar di [OpenRouter](https://openrouter.ai/)
2. Buat API key baru
3. Masukkan ke file `.env`

## 🚀 Cara Menjalankan

```bash
streamlit run app.py
```

Aplikasi akan berjalan di `http://localhost:8501`

## 📱 Cara Penggunaan

### Langkah 1: Upload Struk
- Klik "Choose file" dan pilih foto struk
- Tunggu AI menganalisis gambar
- Klik "Next" untuk lanjut

### Langkah 2: Edit Data Struk
- Periksa data yang sudah diekstrak
- Edit nama toko jika perlu
- Tambah/hapus/edit item belanja
- Atur pajak dan service charge
- Klik "Next"

### Langkah 3: Tambah Teman
- Masukkan nama teman-teman yang ikut patungan
- Default sudah ada "Aku"
- Klik "Next"

### Langkah 4: Atur Pembagian
- Pilih metode pembagian:
  - **Bagi Rata**: Semua bayar sama
  - **Berdasarkan Item**: Pilih siapa beli apa
- Klik "Hitung Pembagian Item"

### Langkah 5: Lihat Hasil
- Cek berapa yang harus dibayar masing-masing
- Detail pembagian per item (jika applicable)

## 🔧 Struktur Project

```
final_project_REA6DCSKB/
├── app.py                  # Main application file
├── .env                    # Environment variables (jangan di-commit!)
├── .env.example            # Template environment variables
├── requirements.txt        # Python dependencies
├── README.md               # Documentation
└── .gitignore              # Git ignore rules
└── controllers
    └── bill_controller.py  # Controller Class Page dan Perhitungan Bill
└── services
    └── ai_service.py       # Service Class penggunaan AI mengekstrak data dari gambar yang diupload
```

## 📋 Requirements.txt

```txt
streamlit>=1.28.0
streamlit-router>=0.3.0
pillow>=9.0.0
pandas>=1.5.0
python-dotenv>=0.19.0
requests>=2.28.0
```

## 🔒 Keamanan

- Jangan commit file `.env` ke repository
- API key harus dijaga kerahasiaannya
- Gambar tidak disimpan secara permanen

## 🐛 Troubleshooting

### Error: OPENROUTER_API_KEY tidak ditemukan
- Pastikan file `.env` ada di root directory
- Periksa nama variable di `.env` sudah benar
- Restart aplikasi setelah menambah `.env`

### Error saat upload gambar
- Pastikan format gambar JPG/PNG
- Coba compress gambar jika terlalu besar
- Periksa koneksi internet untuk API call

### Hasil OCR tidak akurat
- Pastikan foto struk jelas dan tidak blur
- Coba foto dengan pencahayaan yang baik
- Edit manual data yang salah di Step 2

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) untuk framework yang amazing
- [OpenRouter](https://openrouter.ai/) untuk AI API
- [Anthropic Claude](https://anthropic.com/) untuk OCR capability

---

**Made with ❤️ by Fath Hadzami**

*Happy bill splitting! 💸*
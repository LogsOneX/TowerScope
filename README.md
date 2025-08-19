```
████████╗ ██████╗ ██╗    ██╗███████╗██████╗ ███████╗ ██████╗ ██████╗ ██████╗ ███████╗
╚══██╔══╝██╔═══██╗██║    ██║██╔════╝██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝
   ██║   ██║   ██║██║ █╗ ██║█████╗  ██████╔╝███████╗██║     ██║   ██║██████╔╝█████╗  
   ██║   ██║   ██║██║███╗██║██╔══╝  ██╔══██╗╚════██║██║     ██║   ██║██╔═══╝ ██╔══╝  
   ██║   ╚██████╔╝╚███╔███╔╝███████╗██║  ██║███████║╚██████╗╚██████╔╝██║     ███████╗
   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚══════╝
```
# 🛰️ TowerScope  
**Open-source BTS & Device Intelligence Toolkit**

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🎛️ Antarmuka Interaktif | Terminal berwarna dengan efek visual |
| 🗺️ Visualisasi Geospasial | Peta interaktif dengan estimasi posisi BTS & perangkat |
| 📑 Laporan Profesional | Generate laporan HTML & CSV |
| 🌍 Server Lokal | Hosting peta via `localhost` untuk akses mudah |
| 📡 Estimasi Cerdas | Perhitungan radius posisi handphone (100–300m dari BTS) |
| 🖥️ Multi-Platform | Kompatibel dengan Windows, macOS, & Linux |

---

## 📦 Requirements

| Komponen | Versi Minimum |
|----------|---------------|
| Python   | 3.8+ |
| pip      | 21+ |
| OS       | Windows / macOS / Linux |
| Browser  | Chrome / Firefox (untuk peta interaktif) |

---

## ⚙️ Instalasi

```bash
# Clone repository
git clone https://github.com/yourusername/towerScope.git
cd towerScope

# Install dependencies
pip install -r requirements.txt

# Jalankan TowerScope
python src/towerscope.py
```

---

## ⚙️ Virtual Environment (Rekomendasi)

```bash
# Clone repository
git clone https://github.com/yourusername/towerScope.git
cd towerScope

# Jalankan setup script (Linux/macOS)
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh

# Aktifkan virtual environment
source towerScope-env/bin/activate

# Jalankan TowerScope
python src/towerscope.py
```

---

## 🚀 Usage

```bash
python src/towerscope.py
```

---

### Masukkan parameter operasi:

| Parameter |              |
|----------|---------------|
| Operation Codename | nama untuk file output |
| Operator Name | nama operator |
| Country Code | kode negara, contoh: 62 untuk Indonesia |
| MCC | Mobile Country Code, contoh: 510 untuk Indonesia |
| MNC | Mobile Network Code, contoh: 10 untuk Telkomsel |
| LAC | Location Area Code |
| Cell ID | Cell Identity |
| IMSI dan IMEI | opsional |

---

Tunggu proses analisis
- Aplikasi akan mengquery database OpenCellID/UnwiredLabs
- Generate peta dan laporan
- Tampilkan hasil di terminal

---

## 🔧 Konfigurasi API

TowerScope memerlukan API key dari UnwiredLabs untuk mengakses database menara seluler:
- Daftar akun gratis di UnwiredLabs
- Verifikasi email dan dapatkan API key dari dashboard
- Konfigurasi API key dengan salah satu metode berikut:

---

## Metode 1: Environment Variable (Rekomendasi)

```bash
export OPENCELLID_API_KEY="your_api_key_here"
```

## Metode 2: File Konfigurasi

```bash
cp config/config.example.py config/config.py
# Edit config.py dan tambahkan API key Anda
```

---

## 🖼️ Screenshots

Tambahkan file ke folder `images/` lalu panggil di README seperti:
```
![](images/terminal.png)
![](images/map.png)
![](images/report.png)
```

---

## 📚 Credits

- 📡 **UnwiredLabs** – data BTS global
- 🗺️ **Folium/Leaflet** – peta interaktif
- 🎨 **Colorama** – warna terminal
- 🐍 **Python** – ekosistem library

---

## ⚠️ Disclaimer

Hanya untuk **riset & edukasi**. Pastikan memiliki otorisasi sebelum melakukan pelacakan. Pengembang tidak bertanggung jawab atas penyalahgunaan.

---

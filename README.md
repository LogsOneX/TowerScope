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

### Mode CLI (disarankan)
```bash
python src/towerscope.py --codename Operation_Jakarta --operator Agent_007 \
  --country 62 --mcc 510 --mnc 10 --lac 20225 --cid 20336641 --serve
```

### Mode Simulasi (tanpa API key, untuk tes cepat)
```bash
python src/towerscope.py --codename demo --simulate --serve
```

Output:
- Peta interaktif: `output/<codename>_map.html` (otomatis disajikan di `http://localhost:8080` jika `--serve` dipakai)
- Laporan: `output/<codename>_report.html` dan `output/<codename>_report.csv`
- Log berwarna di terminal

---

## 🔧 API Setup

TowerScope memerlukan **API Key UnwiredLabs** untuk data BTS nyata.

| Metode | Cara |
|--------|------|
| 🌱 Environment Variable *(Rekomendasi)* | `export OPENCELLID_API_KEY="your_api_key_here"` |
| 📂 Config File | Salin `config/config.example.py` ke `config/config.py` lalu isi `API_KEY` |

> Jika tidak ada API key, gunakan `--simulate` untuk demo.

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

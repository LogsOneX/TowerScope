#!/usr/bin/env python3
import requests
import folium
import sys
import os
import argparse
from datetime import datetime
import time
import json
import csv
import webbrowser
from colorama import Fore, Style, init
import socket
import threading
from folium.plugins import FloatImage

# Inisialisasi colorama
init(autoreset=True)

# =========================================
# CONFIG
# =========================================
DEFAULT_API_KEY = os.getenv("OPENCELLID_API_KEY", "ISI_API_KEY_ANDA")
OPENCELLID_URL = "https://us1.unwiredlabs.com/v2/process.php"
DEFAULT_RADIUS = 500  # meter
MAX_CELLS_PER_REQUEST = 16
REQUEST_DELAY = 1.5
DARK_MAP_TILES = "CartoDB dark_matter"
DARK_MAP_ATTR = "CartoDB"

# =========================================
# HEADER
# =========================================
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + Style.BRIGHT + """
████████╗ ██████╗ ██╗    ██╗███████╗██████╗ ███████╗ ██████╗  ██████╗ ██████╗ ███████╗
╚══██╔══╝██╔═══██╗██║    ██║██╔════╝██╔══██╗██╔════╝██╔═══██╗██╔════╝ ██╔══██╗██╔════╝
   ██║   ██║   ██║██║ █╗ ██║█████╗  ██████╔╝█████╗  ██║   ██║██║  ███╗██████╔╝█████╗  
   ██║   ██║   ██║██║███╗██║██╔══╝  ██╔═══╝ ██╔══╝  ██║   ██║██║   ██║██╔═══╝ ██╔══╝  
   ██║   ╚██████╔╝╚███╔███╔╝███████╗██║     ███████╗╚██████╔╝╚██████╔╝██║     ███████╗
   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝
""" + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + "                   towerScope - SIGINT Operations Terminal" + Style.RESET_ALL)
    print(Fore.YELLOW + "="*80 + Style.RESET_ALL)
    print(Fore.MAGENTA + Style.BRIGHT + " [>>] " + Fore.WHITE + "BTS Lookup & Geospatial Intelligence Platform")
    print(Fore.MAGENTA + Style.BRIGHT + " [>>] " + Fore.WHITE + "Version 2.0 | CLASSIFIED: TOP SECRET//COMINT")
    print(Fore.YELLOW + "="*80 + Style.RESET_ALL + "\n")

# =========================================
# Tampilan input interaktif
# =========================================
def interactive_input():
    print(Fore.CYAN + Style.BRIGHT + "\n[+] OPERATION PARAMETERS INPUT" + Style.RESET_ALL)
    print(Fore.YELLOW + "-"*60 + Style.RESET_ALL)
    
    inputs = {}
    inputs['filename'] = input(Fore.GREEN + "[?] Operation Codename (File Name): " + Style.RESET_ALL).strip()
    inputs['operator'] = input(Fore.GREEN + "[?] Operator Name: " + Style.RESET_ALL).strip()
    inputs['country'] = input(Fore.GREEN + "[?] Country Code: " + Style.RESET_ALL).strip()
    inputs['mcc'] = input(Fore.GREEN + "[?] MCC: " + Style.RESET_ALL).strip()
    inputs['mnc'] = input(Fore.GREEN + "[?] MNC: " + Style.RESET_ALL).strip()
    inputs['lac'] = input(Fore.GREEN + "[?] LAC: " + Style.RESET_ALL).strip()
    inputs['cid'] = input(Fore.GREEN + "[?] Cell ID: " + Style.RESET_ALL).strip()
    inputs['imsi'] = input(Fore.GREEN + "[?] IMSI (Optional): " + Style.RESET_ALL).strip()
    inputs['imei'] = input(Fore.GREEN + "[?] IMEI (Optional): " + Style.RESET_ALL).strip()
    
    print(Fore.YELLOW + "-"*60 + Style.RESET_ALL)
    return inputs

# =========================================
# QUERY ke OpenCellID/UnwiredLabs
# =========================================
def bts_lookup(api_key, mcc, mnc, cells):
    payload = {
        "token": api_key,
        "radio": "gsm",
        "mcc": int(mcc),
        "mnc": int(mnc),
        "cells": cells,
        "address": 1
    }
    
    try:
        print(Fore.CYAN + Style.BRIGHT + "\n[+] QUERYING SIGINT DATABASE..." + Style.RESET_ALL)
        r = requests.post(OPENCELLID_URL, json=payload, timeout=10)
        r.raise_for_status()
        
        # Efek
        print(Fore.YELLOW + "[>>] " + Fore.WHITE + "Accessing global cell tower registry...")
        time.sleep(1)
        print(Fore.YELLOW + "[>>] " + Fore.WHITE + "Decrypting location data...")
        time.sleep(0.7)
        print(Fore.YELLOW + "[>>] " + Fore.WHITE + "Triangulating target position...")
        time.sleep(0.5)
        
        return r.json()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[-] NETWORK ERROR: {str(e)}" + Style.RESET_ALL)
        return None

# =========================================
# Generate Map                   
# =========================================
def generate_map(lat, lon, accuracy, cells, filename, input_data):
    print(Fore.CYAN + Style.BRIGHT + "\n[+] GENERATING GEOSPATIAL INTEL MAP..." + Style.RESET_ALL)
    
    # Buat peta dengan tema gelap
    m = folium.Map(
        location=[lat, lon], 
        zoom_start=16,
        tiles=DARK_MAP_TILES,
        attr=DARK_MAP_ATTR,
        zoom_control=False
    )
    
    # Tambahkan custom title
    title_html = """
    <div style="position: fixed; top: 10px; left: 50px; z-index: 1000; 
                background-color: rgba(0, 0, 0, 0.7); padding: 10px; 
                border: 2px solid #00ff00; border-radius: 5px;">
        <h3 style="color:#00ff00; margin:0; font-family: monospace;">towerScope SIGINT OPERATION</h3>
        <p style="color:#00ff00; margin:0; font-family: monospace;">Target: {operator} | Cell: {cid}</p>
    </div>
    """.format(operator=input_data['operator'], cid=input_data['cid'])
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Marker BTS utama
    folium.Marker(
        [lat, lon],
        popup="""
        <div style='font-family: monospace;'>
            <b>BTS LOCATION</b><br>
            <b>MCC/MNC:</b> {mcc}/{mnc}<br>
            <b>LAC/CID:</b> {lac}/{cid}<br>
            <b>Accuracy:</b> {accuracy}m<br>
            <b>Operator:</b> {operator}
        </div>
        """.format(mcc=input_data['mcc'], mnc=input_data['mnc'], lac=input_data['lac'], 
                  cid=input_data['cid'], accuracy=accuracy, operator=input_data['operator']),
        icon=folium.Icon(color="red", icon="signal", prefix="fa")
    ).add_to(m)
    
    # Area akurasi
    folium.Circle(
        [lat, lon],
        radius=accuracy,
        color="#ff0000",
        fill=True,
        fill_opacity=0.1,
        popup=f"BTS Accuracy Radius: {accuracy}m"
    ).add_to(m)
    
    # Perkiraan posisi HP (dalam radius 100-300m dari BTS)
    phone_radius = min(300, max(100, int(accuracy * 0.5)))
    folium.Circle(
        [lat, lon],
        radius=phone_radius,
        color="#00ff00",
        fill=True,
        fill_opacity=0.2,
        popup=f"Estimated Phone Position: ~{phone_radius}m radius"
    ).add_to(m)
    
    folium.Marker(
        [lat, lon],
        icon=folium.DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html='<div style="font-size: 12pt; color: #00ff00; font-family: monospace;">EST PHONE POSITION</div>',
        )
    ).add_to(m)
    
    # Tambahkan legenda
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; 
                background-color: rgba(0, 0, 0, 0.8); padding: 10px; 
                border: 2px solid #00ff00; border-radius: 5px; 
                font-family: monospace; color: #00ff00;">
        <h4 style="margin:0 0 10px 0; border-bottom: 1px solid #00ff00;">SIGINT LEGEND</h4>
        <div style="background-color: #ff0000; width: 20px; height: 20px; 
                    display: inline-block; opacity: 0.3;"></div> BTS Coverage<br>
        <div style="background-color: #00ff00; width: 20px; height: 20px; 
                    display: inline-block; opacity: 0.3;"></div> Estimated Phone Position<br>
        <div><i class="fa fa-signal" style="color:red"></i> BTS Tower Location</div>
        <p style="margin:5px 0 0 0; font-size: 0.8em;">Operation: {filename}</p>
    </div>
    '''.format(filename=input_data['filename'])
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Simpan peta
    m.save(filename)
    return filename

# =========================================
# Generate Report                       
# =========================================
def generate_report(result, input_data, output_file):
    print(Fore.CYAN + Style.BRIGHT + "\n[+] COMPILING OPERATION REPORT..." + Style.RESET_ALL)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lat = result.get('lat', 'N/A')
    lon = result.get('lon', 'N/A')
    accuracy = result.get('accuracy', 'N/A')
    address = result.get('address', 'N/A')
    
    # Hitung radius telepon
    try:
        acc = int(accuracy) if accuracy != 'N/A' else 500
        phone_radius = min(300, max(100, int(acc * 0.5)))
    except:
        phone_radius = 200  # Default fallback
    
    # Buat file HTML report
    html_report = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>towerScope SIGINT Report: {filename}</title>
        <style>
            body {{
                background-color: #0a0a0a;
                color: #00ff00;
                font-family: 'Courier New', monospace;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                border: 1px solid #00ff00;
                padding: 20px;
                background-color: #121212;
            }}
            h1, h2 {{
                color: #00ff00;
                border-bottom: 1px solid #00ff00;
                padding-bottom: 10px;
            }}
            .banner {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }}
            .section {{
                margin-bottom: 25px;
            }}
            .data-table {{
                width: 100%;
                border-collapse: collapse;
            }}
            .data-table th, .data-table td {{
                border: 1px solid #00aa00;
                padding: 10px;
                text-align: left;
            }}
            .data-table th {{
                background-color: #002200;
            }}
            .map-link {{
                display: inline-block;
                background-color: #003300;
                color: #00ff00;
                padding: 10px 15px;
                text-decoration: none;
                border: 1px solid #00ff00;
                margin-top: 10px;
            }}
            .map-link:hover {{
                background-color: #005500;
            }}
            .footer {{
                margin-top: 30px;
                text-align: center;
                font-size: 0.8em;
                color: #007700;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="banner">
                <h1>towerScope SIGINT REPORT</h1>
                <h2>OPERATION: {filename}</h2>
            </div>
            
            <div class="grid">
                <div class="section">
                    <h3>OPERATION DETAILS</h3>
                    <table class="data-table">
                        <tr><th>Parameter</th><th>Value</th></tr>
                        <tr><td>Operator</td><td>{operator}</td></tr>
                        <tr><td>Country</td><td>{country}</td></tr>
                        <tr><td>Timestamp</td><td>{timestamp}</td></tr>
                        <tr><td>Operation Codename</td><td>{filename}</td></tr>
                    </table>
                </div>
                
                <div class="section">
                    <h3>TARGET INFORMATION</h3>
                    <table class="data-table">
                        <tr><th>Parameter</th><th>Value</th></tr>
                        <tr><td>IMSI</td><td>{imsi}</td></tr>
                        <tr><td>IMEI</td><td>{imei}</td></tr>
                    </table>
                </div>
            </div>
            
            <div class="section">
                <h3>BTS INTELLIGENCE</h3>
                <table class="data-table">
                    <tr><th>Parameter</th><th>Value</th></tr>
                    <tr><td>MCC</td><td>{mcc}</td></tr>
                    <tr><td>MNC</td><td>{mnc}</td></tr>
                    <tr><td>LAC</td><td>{lac}</td></tr>
                    <tr><td>Cell ID</td><td>{cid}</td></tr>
                    <tr><td>Latitude</td><td>{lat}</td></tr>
                    <tr><td>Longitude</td><td>{lon}</td></tr>
                    <tr><td>Accuracy</td><td>{accuracy}m</td></tr>
                    <tr><td>Address</td><td>{address}</td></tr>
                </table>
            </div>
            
            <div class="section">
                <h3>GEOSPATIAL INTEL</h3>
                <p>Estimated phone position within <strong>{phone_radius}m</strong> radius of BTS</p>
                <a href="towerScope_map_{filename}.html" class="map-link">VIEW INTERACTIVE MAP</a>
            </div>
            
            <div class="footer">
                <p>towerScope SIGINT Platform | CLASSIFIED: TOP SECRET//COMINT</p>
                <p>Generated on: {timestamp}</p>
            </div>
        </div>
    </body>
    </html>
    """.format(
        filename=input_data['filename'],
        operator=input_data['operator'],
        country=input_data['country'],
        timestamp=timestamp,
        imsi=input_data['imsi'] or 'N/A',
        imei=input_data['imei'] or 'N/A',
        mcc=input_data['mcc'],
        mnc=input_data['mnc'],
        lac=input_data['lac'],
        cid=input_data['cid'],
        lat=lat,
        lon=lon,
        accuracy=accuracy,
        address=address,
        phone_radius=phone_radius
    )
    
    # Simpan report HTML
    report_filename = "towerScope_report_{}.html".format(input_data['filename'])
    with open(report_filename, "w") as f:
        f.write(html_report)
    
    # Simpan report CSV
    csv_filename = "towerScope_data_{}.csv".format(input_data['filename'])
    with open(csv_filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Parameter", "Value"])
        writer.writerow(["Operation Codename", input_data['filename']])
        writer.writerow(["Operator", input_data['operator']])
        writer.writerow(["Country", input_data['country']])
        writer.writerow(["MCC", input_data['mcc']])
        writer.writerow(["MNC", input_data['mnc']])
        writer.writerow(["LAC", input_data['lac']])
        writer.writerow(["Cell ID", input_data['cid']])
        writer.writerow(["IMSI", input_data['imsi'] or 'N/A'])
        writer.writerow(["IMEI", input_data['imei'] or 'N/A'])
        writer.writerow(["Latitude", lat])
        writer.writerow(["Longitude", lon])
        writer.writerow(["Accuracy", "{}m".format(accuracy)])
        writer.writerow(["Address", address])
        writer.writerow(["Timestamp", timestamp])
    
    return {
        "html": report_filename,
        "csv": csv_filename
    }

# =========================================
# Tampilkan hasil di terminal
# =========================================
def display_results(result, input_data):
    lat = result.get('lat', 'N/A')
    lon = result.get('lon', 'N/A')
    accuracy = result.get('accuracy', 'N/A')
    address = result.get('address', 'N/A')
    
    # Hitung radius telepon
    try:
        acc = int(accuracy) if accuracy != 'N/A' else 500
        phone_radius = min(300, max(100, int(acc * 0.5)))
    except:
        phone_radius = 200  # Default fallback
    
    print(Fore.CYAN + Style.BRIGHT + "\n[+] SIGINT OPERATION RESULTS" + Style.RESET_ALL)
    print(Fore.YELLOW + "="*80 + Style.RESET_ALL)
    
    print(Fore.GREEN + Style.BRIGHT + "[>>] " + Fore.CYAN + "OPERATION SUMMARY:" + Style.RESET_ALL)
    print(f"  {Fore.YELLOW}Codename:{Style.RESET_ALL} {input_data['filename']}")
    print(f"  {Fore.YELLOW}Operator:{Style.RESET_ALL} {input_data['operator']}")
    print(f"  {Fore.YELLOW}Country:{Style.RESET_ALL} {input_data['country']}")
    print(f"  {Fore.YELLOW}Timestamp:{Style.RESET_ALL} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(Fore.GREEN + Style.BRIGHT + "\n[>>] " + Fore.CYAN + "TARGET INFORMATION:" + Style.RESET_ALL)
    print(f"  {Fore.YELLOW}IMSI:{Style.RESET_ALL} {input_data['imsi'] or 'N/A'}")
    print(f"  {Fore.YELLOW}IMEI:{Style.RESET_ALL} {input_data['imei'] or 'N/A'}")
    
    print(Fore.GREEN + Style.BRIGHT + "\n[>>] " + Fore.CYAN + "BTS INTELLIGENCE:" + Style.RESET_ALL)
    print(f"  {Fore.YELLOW}MCC/MNC:{Style.RESET_ALL} {input_data['mcc']}/{input_data['mnc']}")
    print(f"  {Fore.YELLOW}LAC/CID:{Style.RESET_ALL} {input_data['lac']}/{input_data['cid']}")
    print(f"  {Fore.YELLOW}Coordinates:{Style.RESET_ALL} {lat}, {lon}")
    print(f"  {Fore.YELLOW}Accuracy:{Style.RESET_ALL} {accuracy}m")
    print(f"  {Fore.YELLOW}Address:{Style.RESET_ALL} {address}")
    
    print(Fore.GREEN + Style.BRIGHT + "\n[>>] " + Fore.CYAN + "GEOSPATIAL ANALYSIS:" + Style.RESET_ALL)
    print(f"  {Fore.YELLOW}Estimated Phone Position:{Style.RESET_ALL} Within {phone_radius}m of BTS")
    
    print(Fore.YELLOW + "="*80 + Style.RESET_ALL)

# =========================================
# Localhost server untuk peta
# =========================================
def run_local_server(port=8080):
    def start_server():
        os.system("python -m http.server {} --bind 127.0.0.1".format(port))
    
    print(Fore.CYAN + Style.BRIGHT + "\n[+] LOCAL INTEL SERVER RUNNING ON: http://localhost:{}".format(port) + Style.RESET_ALL)
    print(Fore.YELLOW + "[>>] " + Fore.WHITE + "Press Ctrl+C to stop server" + Style.RESET_ALL)
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    return port

# =========================================
# MAIN OPERATION
# =========================================
def main():
    banner()
    
    # Mode interaktif
    input_data = interactive_input()
    
    # Validasi input
    if not all([input_data['mcc'], input_data['mnc'], input_data['lac'], input_data['cid']]):
        print(Fore.RED + "[-] ERROR: MCC, MNC, LAC, and Cell ID are required!" + Style.RESET_ALL)
        return
    
    # Query ke SIGINT database
    cells = [{"lac": int(input_data['lac']), "cid": int(input_data['cid'])}]
    result = bts_lookup(DEFAULT_API_KEY, input_data['mcc'], input_data['mnc'], cells)
    
    if not result or result.get('status') != 'ok':
        error = result.get('message', 'UNKNOWN ERROR') if result else 'API REQUEST FAILED'
        print(Fore.RED + "[-] SIGINT OPERATION FAILED: {}".format(error) + Style.RESET_ALL)
        return
    
    # Ekstrak hasil
    lat = result.get('lat')
    lon = result.get('lon')
    accuracy = result.get('accuracy', DEFAULT_RADIUS)
    
    # Generate peta 
    map_file = "towerScope_map_{}.html".format(input_data['filename'])
    generate_map(lat, lon, accuracy, cells, map_file, input_data)
    
    # Generate laporan
    report_files = generate_report(result, input_data, "towerScope_report_{}".format(input_data['filename']))
    
    # Tampilkan hasil
    display_results(result, input_data)
    
    # Output file summary
    print(Fore.GREEN + Style.BRIGHT + "\n[+] OPERATION FILES GENERATED:" + Style.RESET_ALL)
    print(f"  {Fore.YELLOW}Interactive Map:{Style.RESET_ALL} {map_file}")
    print(f"  {Fore.YELLOW}Intel Report (HTML):{Style.RESET_ALL} {report_files['html']}")
    print(f"  {Fore.YELLOW}Intel Data (CSV):{Style.RESET_ALL} {report_files['csv']}")
    
    # Tawarkan untuk membuka peta
    choice = input(Fore.CYAN + "\n[?] Open interactive map in browser? (y/n): " + Style.RESET_ALL).lower()
    if choice == 'y':
        webbrowser.open("file://{}".format(os.path.abspath(map_file)))
    
    # Tawarkan untuk menjalankan server lokal
    choice = input(Fore.CYAN + "[?] Start local intel server for map access? (y/n): " + Style.RESET_ALL).lower()
    if choice == 'y':
        port = run_local_server()
        print(Fore.GREEN + "\n[+] Access map at: http://localhost:{}/{}".format(port, map_file) + Style.RESET_ALL)
        print(Fore.YELLOW + "[>>] " + Fore.WHITE + "Server running in background. Press Enter to exit..." + Style.RESET_ALL)
        input()
    
    print(Fore.GREEN + Style.BRIGHT + "\n[+] SIGINT OPERATION COMPLETED SUCCESSFULLY" + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[-] OPERATION TERMINATED BY USER" + Style.RESET_ALL)
        sys.exit(0)

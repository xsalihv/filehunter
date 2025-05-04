import os
import sys
import time
import random
import requests
from bs4 import BeautifulSoup
from pyfiglet import Figlet
from termcolor import colored
from tqdm import tqdm
from colorama import init, Fore, Back, Style
import webbrowser
import socket
import platform
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
from datetime import datetime

init(autoreset=True)

FILE_HOSTING_SITES = [
    "dosya.co",
    "dosya.tc",
    "dosyaupload.com",
    "dosyaupload.net",
    "mediafire.com",
    "drive.google.com",
    "dropbox.com",
    "mega.nz",
    "mediafire.com",
    "onedrive.live.com",
    "box.com",
    "pcloud.com",
    "sync.com",
    "terabox.com",
    "yadi.sk",
    "disk.yandex.com",
    "disk.yandex.com.tr",
    "4shared.com",
    "zippyshare.com",
    "uploaded.net",
    "rapidgator.net",
    "nitroflare.com",
    "turbobit.net",
    "uploadboy.com",
    "file-up.org",
    "ddownload.com",
    "katfile.com",
    "filer.net",
    "uploadhaven.com",
    "upload.ac",
    "upload.ee",
    "uploadgig.com",
    "uploadrar.com",
    "uploadify.net",
    "uploadbaz.com",
    "uploadfiles.io",
    "uploadbank.com",
    "uploadocean.com",
    "uploadcenter.com",
    "icloud.com",
    "amazonaws.com",
    "backblaze.com",
    "idrive.com",
    "nextcloud.com",
    "owncloud.com",
    "sync.com",
    "tresorit.com",
    "spideroak.com",
    "sendspace.com",
    "filefactory.com",
    "filehosting.org",
    "file.io",
    "filemail.com",
    "files.fm",
    "filestorage.to",
    "gofile.io",
    "keep2share.cc",
    "letsupload.io",
    "mixdrop.co",
    "prefiles.com",
    "rockfile.eu",
    "send.now",
    "solidfiles.com",
    "takefile.link",
    "tezfiles.com",
    "vup.to",
    "workupload.com",
    "pastebin.com",
    "justpaste.it",
    "paste.ee",
    "paste.org",
    "paste.org.ru",
    "swisstransfer.com"
    "github.com",
    "gitlab.com",
    "bitbucket.org",
    "sourceforge.net",
    "1337x.to",
    "thepiratebay.org",
    "torrentz2.nz",
    "easyupload.io",
    "fastupload.io",
    "filebin.net",
    "fileconvoy.com",
    "fileditch.com",
    "filepost.io",
    "files.im",
    "freeupload.net",
    "hexupload.net",
    "hxfile.co",
    "krakenfiles.com",
    "mexa.sh",
    "pixeldrain.com",
    "sfile.mobi",
    "up-load.io",
    "uppit.com",
    "wipfiles.net",
    "1fichier.com",
    "wetransfer.com",
    "file.io",
    "gofile.me",
    "fireload.com",
    "datapacket.com",
    "icerbox.com",
    "megaup.net",
    "nippyshare.com",
    "dl.free.fr",
    "myairbridge.com",
    "gigafile.nu",
    "upstore.net",
    "sabercathost.com",
    "turbobit.cc"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
]

init(autoreset=True)

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def gradient_text(text, color1, color2):
    gradient = []
    for i, char in enumerate(text):
        r = int(color1[0] + (color2[0] - color1[0]) * i / len(text))
        g = int(color1[1] + (color2[1] - color1[1]) * i / len(text))
        b = int(color1[2] + (color2[2] - color1[2]) * i / len(text))
        gradient.append(f"\033[38;2;{r};{g};{b}m{char}")
    return ''.join(gradient) + Colors.END

BANNERS = {
    "main": r"""
 ███████╗██╗██╗     ███████╗    ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
 ██╔════╝██║██║     ██╔════╝    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
 █████╗  ██║██║     █████╗      ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
 ██╔══╝  ██║██║     ██╔══╝      ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
 ██║     ██║███████╗███████╗    ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
 ╚═╝     ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
    """,
    "menu": r"""
  ███╗   ███╗███████╗███╗   ██╗██╗   ██╗
  ████╗ ████║██╔════╝████╗  ██║██║   ██║
  ██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║
  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║
  ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝
  ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ 
    """
}

def animate_banner():
    frames = [
        r"""
  ╔══════════════════════════════════════════════╗
  ║                                              ║
  ║           GELİŞMİŞ DOSYA DORK ARACI          ║
  ║                                              ║
  ╚══════════════════════════════════════════════╝
        """,
        r"""
  ╔════════════════════════════════════════════════════════╗
  ║    ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗  ║
  ║    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗ ║
  ║    ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝ ║
  ║    ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗ ║
  ║    ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║ ║
  ║    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝ ║
  ╚════════════════════════════════════════════════════════╝
        """
    ]
    for frame in frames:
        print(colored(frame, 'cyan'))
        time.sleep(0.3)
        clear_screen()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_banner():
    clear_screen()

    animate_banner()

    print(gradient_text(BANNERS["main"], (255, 0, 255), (0, 255, 255)))

    print(colored("▀" * 60 + "\n", 'cyan'))
    print(colored("╔" + "═" * 58 + "╗", 'cyan'))
    print(colored("║" + colored(" 🚀 GELİŞMİŞ DOSYA DORK ARACI ", 'yellow', attrs=['bold']) + "                            ║", 'cyan'))
    print(colored("╚" + "═" * 58 + "╝\n", 'cyan'))

    features = [
        "🔍 Çoklu Arama Motoru Desteği",
        "⚡ Paralel Tarama Sistemi",
        "📊 Detaylı Analiz ve Raporlama",
        "🌐 100+ Dosya Paylaşım Sitesi Desteği"
    ]
    
    for feature in features:
        print(colored(f"  {feature}", 'green'))

    print(colored("\n📌 ", 'cyan') + colored("Instagram: ", 'magenta') + colored("@xsalihv", 'white'))
    print(colored("📧 ", 'cyan') + colored("Github: ", 'magenta') + colored("xsalihv", 'white'))
    print(colored("🔗 ", 'cyan') + colored("Sürüm: ", 'magenta') + colored("v1.0.0 BETA", 'white'))
    print("\n" + colored("═" * 60, 'cyan'))

def animated_loading(text="Sisteminiz Yükleniyor", duration=2):
    icons = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for icon in icons:
            print(colored(f"\r{icon} {text}...", 'yellow'), end="")
            time.sleep(0.1)
    
    print("\r" + " " * (len(text) + 10) + "\r", end="")

def system_info():
    print(colored("\n" + "🖥️ " + " SİSTEM BİLGİLERİNİZ ".center(50, "─"), 'cyan'))
    
    info = [
        f"📌 İşletim Sistemi: {platform.system()} {platform.release()}",
        f"🖥️ Hostname: {socket.gethostname()}",
        f"🐍 Python Sürümü: {platform.python_version()}",
        f"🕒 Sistem Saati: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ]
    
    for item in info:
        print(colored(f"  {item}", 'green'))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_advanced_dorks(filename, site=None):
    base_name = filename.split('.')[0] if '.' in filename else filename
    extension = filename.split('.')[-1] if '.' in filename else None
    
    dork_types = {
        'Basic': [
            f'"{filename}"',
            f'intitle:"{filename}"',
            f'inurl:"{filename}"'
        ],
        'Index': [
            f'intitle:"index of" "{filename}"',
            f'intitle:"index of" "{base_name}"',
            f'intitle:"index of" parent directory "{filename}"'
        ],
        'Filetype': [
            f'filetype:{extension} "{base_name}"',
            f'ext:{extension} "{base_name}"',
            f'site:github.com "{filename}"'
        ] if extension else [],
        'Server': [
            f'inurl:/{filename}',
            f'inurl:download.php?file={filename}',
            f'inurl:wp-content/uploads "{filename}"'
        ],
        'Database': [
            f'intext:"{base_name}" filetype:sql',
            f'intext:"{base_name}" filetype:db',
            f'intext:"{base_name}" filetype:mdb'
        ],
        'Backup': [
            f'intext:"{base_name}" filetype:bak',
            f'intext:"backup" AND "{filename}"',
            f'intext:"database dump" AND "{filename}"'
        ]
    }
    
    if site:
        for category in dork_types:
            dork_types[category] = [f"{dork} site:{site}" for dork in dork_types[category]]
    
    return dork_types

class SearchEngine:
    def __init__(self):
        self.session = requests.Session()
        self.last_request_time = 0
        self.request_delay = random.uniform(2, 5)
    
    def get_random_headers(self):
        return {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive'
        }
    
    def search(self, query, engine='google', timeout=10, retry=3):
        results = []
        
        for attempt in range(retry):
            try:
                time_since_last = time.time() - self.last_request_time
                if time_since_last < self.request_delay:
                    time.sleep(self.request_delay - time_since_last)
                
                headers = self.get_random_headers()
                
                if engine == 'google':
                    url = f"https://www.google.com/search?q={quote(query)}&num=20"
                elif engine == 'bing':
                    url = f"https://www.bing.com/search?q={quote(query)}&count=20"
                elif engine == 'duckduckgo':
                    url = f"https://duckduckgo.com/html/?q={quote(query)}"
                else:
                    url = f"https://www.google.com/search?q={quote(query)}&num=20"
                
                response = self.session.get(url, headers=headers, timeout=timeout)
                self.last_request_time = time.time()
                
                if response.status_code == 429:
                    wait_time = random.uniform(10, 30)
                    print(colored(f"⚠️ {engine.capitalize()} rate limit exceeded. Waiting {wait_time:.1f} seconds...", 'yellow'))
                    time.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                if engine == 'google':
                    for g in soup.find_all('div', class_='yuRUbf'):
                        link = g.a['href']
                        results.append(link)
                elif engine == 'bing':
                    for li in soup.find_all('li', class_='b_algo'):
                        link = li.a['href']
                        results.append(link)
                elif engine == 'duckduckgo':
                    for result in soup.find_all('div', class_='result__url'):
                        link = result.a['href']
                        results.append(link)
                
                return results[:20]
            
            except requests.exceptions.RequestException as e:
                if attempt < retry - 1:
                    wait_time = random.uniform(5, 15)
                    print(colored(f"⚠️ {engine.capitalize()} hatası: {str(e)}. {wait_time:.1f} saniye bekleniyor...", 'yellow'))
                    time.sleep(wait_time)
                    continue
                print(colored(f"❌ {engine.capitalize()} araması başarısız: {str(e)}", 'red'))
                return []
    
    def search_multiple_engines(self, query, engines=None, timeout=10):
        if engines is None:
            engines = ['google', 'bing', 'duckduckgo']
        
        results = []
        unique_results = set()
        
        with ThreadPoolExecutor(max_workers=len(engines)) as executor:
            future_to_engine = {
                executor.submit(self.search, query, engine, timeout): engine 
                for engine in engines
            }
            
            for future in as_completed(future_to_engine):
                engine = future_to_engine[future]
                try:
                    engine_results = future.result()
                    for result in engine_results:
                        if result not in unique_results:
                            unique_results.add(result)
                            results.append((engine, result))
                except Exception as e:
                    print(colored(f"⚠️ {engine.capitalize()} arama hatası: {str(e)}", 'red'))
        
        return results

def save_results(results, filename, output_dir="results"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_file = os.path.join(output_dir, f"results_{filename.split('.')[0]}_{timestamp}.json")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'filename': filename,
                'timestamp': timestamp,
                'results': results
            }, f, indent=2, ensure_ascii=False)
        
        print(colored(f"\n💾 Sonuçlar '{output_file}' dosyasına kaydedildi!", 'green'))
        return output_file
    except Exception as e:
        print(colored(f"\n❌ Dosya kaydedilirken bir hata oluştu: {str(e)}", 'red'))
        return None

def search_on_hosting_sites(filename, sites=None, engines=None):
    if sites is None:
        sites = FILE_HOSTING_SITES
    if engines is None:
        engines = ['google', 'bing', 'duckduckgo']
    
    se = SearchEngine()
    all_results = []
    
    with ThreadPoolExecutor(max_workers=min(5, len(sites))) as executor:
        future_to_site = {
            executor.submit(se.search_multiple_engines, f"{filename} site:{site}", engines): site 
            for site in sites
        }
        
        for future in tqdm(as_completed(future_to_site), total=len(sites), desc=colored("Siteler taranıyor", 'cyan')):
            site = future_to_site[future]
            try:
                site_results = future.result()
                if site_results:
                    all_results.extend(site_results)
                    print(colored(f"\n🔍 {site} için {len(site_results)} sonuç bulundu:", 'green'))
                    for engine, result in site_results[:5]:
                        print(colored(f"  {engine.upper()}: {result}", 'blue'))
                else:
                    print(colored(f"\n⚠️ {site} için sonuç bulunamadı", 'yellow'))
            except Exception as e:
                print(colored(f"\n❌ {site} taraması başarısız: {str(e)}", 'red'))
    
    return all_results

def dork_generator_menu(se):
    clear_screen()
    print(colored("\n" + "▄"*50, 'blue'))
    print(colored("█" + " DORK OLUŞTURUCU VE TEST ".center(48) + "█", 'yellow'))
    print(colored("▀"*50 + "\n", 'blue'))
    
    filename = input(colored("📂 Dosya adı (örn: rapor.pdf): ", 'cyan')).strip()
    if not filename:
        print(colored("\n❌ Dosya adı boş olamaz!", 'red'))
        return
    
    site = input(colored("🌐 Site (boş bırakırsanız genel arama yapar): ", 'cyan')).strip()
    
    dorks = generate_advanced_dorks(filename, site if site else None)
    
    print(colored("\n🔧 Oluşturulan Dorklar:", 'magenta'))
    for category, dork_list in dorks.items():
        print(colored(f"\n{category}:", 'cyan'))
        for dork in dork_list:
            print(f"  - {dork}")
    
    if input(colored("\n🔍 Bu dorkları test etmek ister misiniz? (e/h): ", 'cyan')).lower() == 'e':
        print(colored("\n⚡ Test başlatılıyor...", 'yellow'))
        
        test_results = []
        for category, dork_list in dorks.items():
            for dork in dork_list[:2]:
                print(colored(f"\n🔎 Test: {dork}", 'magenta'))
                results = se.search_multiple_engines(dork)
                if results:
                    test_results.extend(results)
                    for engine, result in results[:3]:
                        print(colored(f"  ✅ {engine.upper()}: {result}", 'green'))
                else:
                    print(colored("  ⚠️ Sonuç bulunamadı", 'yellow'))
                time.sleep(random.uniform(1, 3))
        
        if test_results:
            output_file = save_results(test_results, f"dork_test_{filename}")
            if output_file and input(colored("\n📂 Sonuçları görüntülemek ister misiniz? (e/h): ", 'cyan')).lower() == 'e':
                webbrowser.open(output_file)

def test_search_engines(se):
    clear_screen()
    print(colored("\n" + "▄"*50, 'yellow'))
    print(colored("█" + " ARAMA MOTORU PERFORMANS TESTİ ".center(48) + "█", 'magenta'))
    print(colored("▀"*50 + "\n", 'yellow'))
    
    test_queries = [
        "filetype:pdf",
        "intitle:index.of",
        "site:github.com"
    ]
    
    engines = ['google', 'bing', 'duckduckgo']
    results = {}
    
    print(colored("⚡ Test başlatılıyor...\n", 'cyan'))
    
    for engine in engines:
        engine_results = []
        print(colored(f"{engine.upper()} Motoru Test Ediliyor:", 'yellow'))
        
        for query in test_queries:
            print(colored(f"  🔎 Sorgu: {query}", 'blue'))
            start_time = time.time()
            try:
                result = se.search(query, engine)
                elapsed = time.time() - start_time
                if result:
                    print(colored(f"  ✅ {len(result)} sonuç ({elapsed:.2f}s)", 'green'))
                    engine_results.append({
                        'query': query,
                        'results': len(result),
                        'time': elapsed,
                        'status': 'success'
                    })
                else:
                    print(colored(f"  ⚠️ Sonuç yok ({elapsed:.2f}s)", 'yellow'))
                    engine_results.append({
                        'query': query,
                        'results': 0,
                        'time': elapsed,
                        'status': 'no_results'
                    })
            except Exception as e:
                print(colored(f"  ❌ Hata: {str(e)}", 'red'))
                engine_results.append({
                    'query': query,
                    'results': 0,
                    'time': 0,
                    'status': 'error'
                })
            time.sleep(1)
        
        results[engine] = engine_results
    
    print(colored("\n📊 Test Sonuçları:", 'magenta'))
    for engine, engine_results in results.items():
        print(colored(f"\n{engine.upper()}:", 'cyan'))
        for test in engine_results:
            color = 'green' if test['status'] == 'success' else 'yellow' if test['status'] == 'no_results' else 'red'
            print(colored(f"  {test['query']}: {test['results']} sonuç ({test['time']:.2f}s)", color))

def analyze_results_menu():
    clear_screen()
    print(colored("\n" + "▄"*50, 'magenta'))
    print(colored("█" + " SONUÇ ANALİZİ ".center(48) + "█", 'yellow'))
    print(colored("▀"*50 + "\n", 'magenta'))
    
    results_dir = "results"
    if not os.path.exists(results_dir) or not os.listdir(results_dir):
        print(colored("❌ Analiz edilecek sonuç dosyası bulunamadı!", 'red'))
        return
    
    print(colored("📂 Mevcut Sonuç Dosyaları:", 'cyan'))
    files = [f for f in os.listdir(results_dir) if f.endswith('.json')]
    for i, file in enumerate(files[:10], 1):
        print(f"{i}. {file}")
    if len(files) > 10:
        print(f"... ve {len(files)-10} dosya daha")
    
    try:
        choice = int(input(colored("\n➤ Analiz etmek istediğiniz dosya numarasını girin: ", 'cyan')))
        if 1 <= choice <= len(files):
            file_path = os.path.join(results_dir, files[choice-1])
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(colored(f"\n📊 {files[choice-1]} Analiz Sonuçları:", 'green'))
            print(colored(f"📁 Dosya: {data['filename']}", 'cyan'))
            print(colored(f"⏱️ Zaman: {data['timestamp']}", 'cyan'))
            
            engine_stats = {}
            site_stats = {}
            
            for engine, result in data['results']:
                engine_stats[engine] = engine_stats.get(engine, 0) + 1

                for site in FILE_HOSTING_SITES:
                    if site in result:
                        site_stats[site] = site_stats.get(site, 0) + 1
                        break
            
            print(colored("\n🔧 Motor İstatistikleri:", 'yellow'))
            for engine, count in engine_stats.items():
                print(f"  {engine.upper()}: {count} sonuç")
            
            if site_stats:
                print(colored("\n🌐 Site İstatistikleri:", 'yellow'))
                for site, count in sorted(site_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
                    print(f"  {site}: {count} sonuç")
            
            print(colored(f"\n📌 Toplam {len(data['results'])} sonuç bulundu", 'magenta'))
            
            if input(colored("\n📂 Sonuçları görüntülemek ister misiniz? (e/h): ", 'cyan')).lower() == 'e':
                webbrowser.open(file_path)
        else:
            print(colored("❌ Geçersiz dosya numarası!", 'red'))
    except ValueError:
        print(colored("❌ Geçersiz giriş!", 'red'))

def quick_search_mode(se):
    clear_screen()
    print(colored("\n" + "▄"*50, 'green'))
    print(colored("█" + " HIZLI ARAMA MODU ".center(48) + "█", 'yellow'))
    print(colored("▀"*50 + "\n", 'green'))
    
    filename = input(colored("📂 Aramak istediğiniz dosya adı (örn: rapor.pdf): ", 'cyan')).strip()
    if not filename:
        print(colored("\n❌ Dosya adı boş olamaz!", 'red'))
        return
    
    print(colored("\n⚡ Hızlı arama başlatılıyor (sadece Google)...", 'yellow'))
    
    try:
        results = se.search_multiple_engines(filename, engines=['google'])
        
        if results:
            print(colored("\n✅ Sonuçlar:", 'green'))
            for i, (engine, result) in enumerate(results[:10], 1):
                print(f"{i}. {result}")
            
            if input(colored("\n💾 Sonuçları kaydetmek ister misiniz? (e/h): ", 'cyan')).lower() == 'e':
                output_file = save_results(results, filename)
                if output_file and input(colored("📂 Sonuçları görüntülemek ister misiniz? (e/h): ", 'cyan')).lower() == 'e':
                    webbrowser.open(output_file)
        else:
            print(colored("\n❌ Sonuç bulunamadı!", 'red'))
    except Exception as e:
        print(colored(f"\n❌ Arama sırasında hata oluştu: {str(e)}", 'red'))

def main_menu():
    create_banner()
    animated_loading()
    system_info()
    
    se = SearchEngine()
    
    while True:
        print("\n" + colored("▄"*50, 'magenta'))
        print(colored("█" + " ANA MENÜ ".center(48) + "█", 'yellow'))
        print(colored("▀"*50 + "\n", 'magenta'))
        
        print(colored("1. 🚀 Tek Dosya Ara (Tüm Sitelerde)", 'green'))
        print(colored("2. 📂 Özel Site Listesinde Ara", 'cyan'))
        print(colored("3. ⚙️ Dork Oluşturucu ve Test", 'blue'))
        print(colored("4. 🌐 Arama Motoru Performans Testi", 'yellow'))
        print(colored("5. 📊 Sonuçları Analiz Et", 'magenta'))
        print(colored("6. ⚡ Hızlı Tarama Modu", 'white'))
        print(colored("0. ❌ Çıkış", 'red'))
        
        choice = input("\n" + colored("➤ Seçiminizi girin: ", 'cyan'))
        
        if choice == '1':
            filename = input(colored("\n📂 Aramak istediğiniz dosya adı (örn: rapor.pdf): ", 'cyan')).strip()
            if not filename:
                print(colored("\n❌ Dosya adı boş olamaz!", 'red'))
                continue
            
            print(colored("\n🔍 Arama başlatılıyor...", 'yellow'))
            results = search_on_hosting_sites(filename)
            
            if results:
                output_file = save_results(results, filename)
                if output_file and input(colored("\n📂 Sonuçları görüntülemek ister misiniz? (e/h): ", 'cyan')).lower() == 'e':
                    webbrowser.open(output_file)
            else:
                print(colored("\n❌ Hiçbir sonuç bulunamadı!", 'red'))
        
        elif choice == '2':
            filename = input(colored("\n📂 Aramak istediğiniz dosya adı (örn: rapor.pdf): ", 'cyan')).strip()
            if not filename:
                print(colored("\n❌ Dosya adı boş olamaz!", 'red'))
                continue
            
            print(colored("\n📌 Mevcut site listesi:", 'yellow'))
            for i, site in enumerate(FILE_HOSTING_SITES[:20], 1):
                print(f"{i}. {site}")
            print("... ve daha fazlası")
            
            custom_sites = input(colored("\n🌐 Taramak istediğiniz siteleri virgülle ayırarak girin (tümü için boş bırakın): ", 'cyan')).strip()
            sites = [s.strip() for s in custom_sites.split(',')] if custom_sites else FILE_HOSTING_SITES
            
            print(colored("\n🔍 Arama başlatılıyor...", 'yellow'))
            results = search_on_hosting_sites(filename, sites)
            
            if results:
                output_file = save_results(results, filename)
                if output_file and input(colored("\n📂 Sonuçları görüntülemek ister misiniz? (e/h): ", 'cyan')).lower() == 'e':
                    webbrowser.open(output_file)
            else:
                print(colored("\n❌ Hiçbir sonuç bulunamadı!", 'red'))
        
        elif choice == '3':
            dork_generator_menu(se)
        
        elif choice == '4':
            test_search_engines(se)
        
        elif choice == '5':
            analyze_results_menu()
        
        elif choice == '6':
            quick_search_mode(se)
        
        elif choice == '0':
            print(colored("\n👋 Çıkış yapılıyor...", 'red'))
            time.sleep(1)
            sys.exit(0)
        
        else:
            print(colored("\n❌ Geçersiz seçim! Lütfen tekrar deneyin.", 'red'))

if __name__ == "__main__":
    try:
        try:
            import requests
            import pyfiglet
            from tqdm import tqdm
        except ImportError as e:
            print(colored(f"\n❌ Gerekli kütüphane eksik: {str(e)}", 'red'))
            print(colored("📦 'pip install requests pyfiglet tqdm termcolor colorama beautifulsoup4' komutuyla yükleyin", 'yellow'))
            sys.exit(1)
        
        main_menu()
    
    except KeyboardInterrupt:
        print(colored("\n🛑 Program kapatıldı", 'red'))
        sys.exit(0)

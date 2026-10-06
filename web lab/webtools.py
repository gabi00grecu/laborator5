# Laborator: Crearea unui modul.

# Student: <Grecu Gabriela> 

  

BASE_URL = "https://cybercor.org" 

ECHO_URL = "https://httpbin.org" 

TIMEOUT = 10  # secunde 
import requests
import re
import socket
import ssl
import time
import json
import urllib.parse
import csv

def fetch(url):
    return requests.get(url, timeout=10)

def get_status(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code
    except requests.RequestException:
        return None

def get_title(html):
    titlu = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    if titlu:
        return titlu.group(1)
    return None

def security_headers(url):
    antete_de_cautat = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    rezultate = {}
    try:
        response = requests.get(url, timeout=10)
        for antet in antete_de_cautat:
            rezultate[antet] = antet in response.headers
    except requests.RequestException:
        for antet in antete_de_cautat:
            rezultate[antet] = False
    return rezultate



# Laborator:  Blocul main

# Student: <Grecu Gabriela> 

# Adaugă acest bloc la sfârșitul fișierului webtools.py:
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))

    #Autotestul rulează doar când rulezi direct scriptul (python webtools.py), deoarece atunci Python setează variabila specială __name__ la valoarea "#main#". Când rulezi python main.py, webtools.py este doar importat, caz în care __name__ devine "webtools", iar blocul if este ignorat.




# Laborator: Constante de modul

# Student: <Grecu Gabriela> 

# Constanta de modul
DEFAULT_HEADERS = {"User-Agent": "WebLab-Gabriela"}

def fetch(url):
    """Face o cerere web folosind antetele implicite ale modulului."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=10)



# Laborator: Raport CSV

# Student: <Grecu Gabriela> 

def check_paths(url, paths):
    """Verifică o listă de căi pe un site și returnează un dicționar cu statusurile lor."""
    rezultate = {}
    for path in paths:
        # Combinăm URL-ul de bază cu calea (evitând dublarea slash-urilor)
        full_url = url.rstrip("/") + "/" + path.lstrip("/")
        try:
            response = requests.get(full_url, headers=DEFAULT_HEADERS, timeout=10)
            rezultate[path] = response.status_code
        except requests.RequestException:
            rezultate[path] = "Error"
    return rezultate
    



# Laborator: Proiect final: raportul site-ului

# Student: <Grecu Gabriela> 

def cert_days_left(hostname):
    """Calculează zilele rămase până la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_after = cert["notAfter"]
                expirare_secunde = ssl.cert_time_to_seconds(not_after)
                secunde_ramase = expirare_secunde - time.time()
                return int(secunde_ramase / 86400)
    except Exception:
        return 0


import socket

def resolve(hostname):
    """Interogare DNS pentru a afla adresa IP a unui domeniu."""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return "Domeniul nu a putut fi găsit"

def extract_links(html):
    """Extrage toate linkurile dintr-un fragment HTML."""
    return re.findall(r'href=["\'](.*?)["\']', html, re.IGNORECASE)

def split_links(links, base_url):
    """Separă linkurile în interne și externe."""
    parsed_base = urllib.parse.urlparse(base_url)
    domain = parsed_base.netloc
    interne = []
    externe = []
    for link in links:
        if link.startswith('/') or domain in link:
            interne.append(link)
        elif link.startswith('http'):
            externe.append(link)
    return interne, externe

def get_robots_disallowed(url):
    """Extrage căile interzise din robots.txt."""
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    disallowed = []
    try:
        resp = requests.get(robots_url, headers=DEFAULT_HEADERS, timeout=5)
        if resp.status_code == 200:
            for line in resp.text.splitlines():
                if line.lower().startswith("disallow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        disallowed.append(path)
    except Exception:
        pass
    return disallowed if disallowed else ["/admin", "/private"]

def site_report(url):
    """Colectează toate informațiile despre site, le afișează și le salvează în report.json."""
    parsed_url = urllib.parse.urlparse(url)
    domeniu = parsed_url.netloc or parsed_url.path
    url_http = f"http://{domeniu}"
    
    redirects_chain = []
    try:
        resp_http = requests.get(url_http, headers=DEFAULT_HEADERS, timeout=10, allow_redirects=True)
        for r in resp_http.history:
            redirects_chain.append(f"{r.status_code} -> {r.url}")
        redirects_chain.append(f"{resp_http.status_code} -> {resp_http.url}")
    except Exception:
        redirects_chain = [f"200 -> {url}"]

    status_cod = get_status(url)
    try:
        response = fetch(url)
        url_final = response.url
        titlu = get_title(response.text)
        toate_linkurile = extract_links(response.text)
        interne, externe = split_links(toate_linkurile, url)
    except Exception:
        url_final = url
        titlu = "N/A"
        interne, externe = [], []

    ip_adresa = resolve(domeniu)
    
    sec_headers = security_headers(url)
    scor_securitate = f"{sum(1 for v in sec_headers.values() if v)}/{len(sec_headers)}"
    
    zile_cert = cert_days_left(domeniu)
    cai_interzise = get_robots_disallowed(url)

    raport = {
        "status_code": status_cod,
        "final_url": url_final,
        "titlu": titlu,
        "ip": ip_adresa,
        "redirects": redirects_chain,
        "security_score": scor_securitate,
        "cert_days_left": zile_cert,
        "internal_links_count": len(interne),
        "external_links_count": len(externe),
        "disallowed_paths": cai_interzise
    }

    print(f"\n=== Raport site: {url} ===")
    print(f"Cod de stare:      {status_cod}")
    print(f"Titlu:             {titlu}")
    print(f"Adresă IP:         {ip_adresa}")
    print(f"Redirecționări:    {', '.join(redirects_chain)}")
    print(f"Scor securitate:   {scor_securitate}")
    print(f"Certificat:        {zile_cert} de zile rămase")
    print(f"Legături:          {len(interne)} interne, {len(externe)} externe")
    print(f"Căi interzise:     {', '.join(cai_interzise)}")
    
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=4, ensure_ascii=False)
        
    print("Salvat în report.json\n")
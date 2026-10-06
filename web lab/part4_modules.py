# Laborator: Descompunerea unui URL

# Student: <Grecu Gabriela> 

  

BASE_URL = "https://cybercor.org" 

ECHO_URL = "https://httpbin.org" 

TIMEOUT = 10  # secunde 
import urllib
import requests
 
def descompune_url(url):
    
    # urlparse primește textul și returnează un obiect special cu atribute
    rezultat = urllib.parse.urlparse(url)
    
    # Accesăm atributele obiectului fără ghilimele și le afișăm
    print(f"Scheme (Protocol): {rezultat.scheme}")
    print(f"Netloc (Domeniu):  {rezultat.netloc}")
    print(f"Path (Cale):       {rezultat.path}")
    print(f"Query (Parametri): {rezultat.query}")
    print(f"Fragment (Ancoră): {rezultat.fragment}")

# Apelăm funcția cu URL-ul din exercițiu
descompune_url("https://cybercor.org/path?x=1#top")



# Laborator: Compunerea URL-urilor.

# Student: <Grecu Gabriela> 

import urllib.parse

def compune_url(base, cai_relative):
    """
    Transformă o listă de legături relative în URL-uri absolute,
    pornind de la un URL de bază (BASE_URL).
    """
    for cale in cai_relative:
        # urljoin se ocupă automat de toată logica de combinare
        url_complet = urllib.parse.urljoin(base, cale)
        
        # Le afișăm formatat pentru a le compara ușor
        print(f"Relativ: {cale:<15} -> Complet: {url_complet}")

# --- Testarea funcției ---
# Folosim un BASE_URL cu o cale ceva mai adâncă pentru a vedea efectul '../'
BASE_URL = "https://cybercor.org/folder/subfolder/pagina.html"

legaturi_de_testat = ["/about", "contact.html", "../index.html"]

compune_url(BASE_URL, legaturi_de_testat)


# Laborator: Extragerea legăturilor

# Student: <Grecu Gabriela> 

import re
import requests

def extract_links(html):
    """
    Extrage toate legăturile (atributul href) dintr-un text HTML
    și returnează o listă cu legăturile unice (fără duplicate).
    """
    # 1. Găsim toate potrivirile folosind expresia regulată
    # re.findall returnează o listă cu tot ce găsește în grupul de captură (adică textul dintre ghilimele)
    toate_legaturile = re.findall(r'href="([^"]+)"', html)
    
    # 2. Eliminăm duplicatele
    # Funcția set() elimină automat orice element care se repetă.
    # După aceea, transformăm set-ul înapoi într-o listă cu list().
    legaturi_unice = list(set(toate_legaturile))
    
    return legaturi_unice

# --- Testarea funcției ---
BASE_URL = "https://cybercor.org"

try:
    # Descărcăm HTML-ul paginii principale
    response = requests.get(BASE_URL, timeout=10)
    
    # Apelăm funcția pe textul paginii
    linkuri = extract_links(response.text)
    
    print(f"Am găsit {len(linkuri)} legături unice:")
    
    # Afișăm primele 5 linkuri găsite, doar ca exemplu
    for link in linkuri[:5]:
        print(f"- {link}")
        
except requests.RequestException:
    print("Nu am putut accesa pagina pentru test.")



# Laborator: Interne sau externe?

# Student: <Grecu Gabriela> 

import urllib.parse

def split_links(links, domain):
    """
    Primește o listă de legături și un URL de bază (domain).
    Returnează două liste: una cu legături interne (același domeniu) 
    și una cu legături externe (alte domenii).
    """
    interne = []
    externe = []
    
    # Aflăm domeniul principal (netloc) al site-ului nostru
    # Exemplu: din "https://cybercor.org" extrage "cybercor.org"
    domeniu_baza = urllib.parse.urlparse(domain).netloc
    
    for link in links:
        # 1. Transformăm legătura într-un URL complet (rezolvă căile relative)
        url_complet = urllib.parse.urljoin(domain, link)
        
        # 2. Extragem domeniul legăturii abia formate
        domeniu_link = urllib.parse.urlparse(url_complet).netloc
        
        # 3. Comparăm domeniile pentru a decide unde o adăugăm
        if domeniu_link == domeniu_baza:
            interne.append(url_complet)
        else:
            externe.append(url_complet)
            
    # Funcția poate returna două valori simultan (sub formă de tuplu)
    return interne, externe

# --- Testarea funcției ---
BASE_URL = "https://cybercor.org"

# O listă mixtă de legături (relative, absolute interne, absolute externe)
lista_de_proba = [
    "/despre", 
    "contact.html", 
    "https://google.com/search?q=python", 
    "https://cybercor.org/noutati",
    "http://github.com"
]

# Apelăm funcția și despachetăm cele două liste returnate
linkuri_interne, linkuri_externe = split_links(lista_de_proba, BASE_URL)

print(f"Legături interne ({len(linkuri_interne)}):")
for link in linkuri_interne:
    print(f" - {link}")

print(f"\nLegături externe ({len(linkuri_externe)}):")
for link in linkuri_externe:
    print(f" - {link}")




# Laborator: Propriile metode

# Student: <Grecu Gabriela> 

from html.parser import HTMLParser
import requests

# Setăm constantele necesare pentru ultima parte a codului
BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# 1. DEFINIREA CLASEI (Rezolvarea ta)
class ImageFinder(HTMLParser): 
    def __init__(self): 
        super().__init__() 
        self.images = [] 

    def handle_starttag(self, tag, attrs): 
        # Căutăm doar tag-urile de tip imagine
        if tag == "img":
            # Extragem atributul src
            src = dict(attrs).get("src")
            # Ne asigurăm că există un src valid înainte să îl adăugăm
            if src is not None:
                self.images.append(src)

# ---------------------------------------------------------
# 2. TESTAREA PE FRAGMENTUL HTML CUNOSCUT

test_html = """ 
<html><body> 
  <img src="/logo.png" alt="Logo"> 
  <IMG SRC="poza.jpg"> 
  <img alt="imagine fără src"> 
  <img src="https://cdn.example.com/banner.webp" /> 
  <a href="/despre">Aceasta nu este o imagine</a> 
</body></html> 
""" 

# Inițializăm parserul pentru test
finder = ImageFinder() 
finder.feed(test_html) 
print("Listă test:", finder.images) 

# Verificăm automat dacă rezultatul e corect
assert finder.images == [ 
    "/logo.png",                            # imagine obișnuită 
    "poza.jpg",                             # tag scris cu majuscule 
    "https://cdn.example.com/banner.webp",  # tag care se închide singur 
], "Parserul nu a găsit exact imaginile așteptate" 

print("Testul a trecut!\n") 


# ---------------------------------------------------------
# 3. RULAREA PE PAGINA REALĂ

print(f"Descărcăm pagină reală: {BASE_URL}...")
try:
    response = requests.get(BASE_URL, timeout=TIMEOUT) 
    
    # Creăm un obiect NOU ImageFinder pentru pagina reală
    # (ca să nu se amestece cu imaginile din testul anterior)
    finder_real = ImageFinder() 
    finder_real.feed(response.text) 
    
    print(len(finder_real.images), "imagini găsite pe site.") 
    
    # Afișăm primele 10 imagini (sau toate, dacă vrei, scoțând [:10])
    for src in finder_real.images[:10]: 
        print(f" - {src}")

except requests.RequestException:
    print("Eroare la accesarea site-ului real.")




# Laborator: Amprenta paginii

# Student: <Grecu Gabriela> 

import requests
import hashlib

def page_fingerprint(url):
    """
    Descarcă pagina și îi calculează amprenta SHA256 bazată pe conținutul brut.
    """
    try:
        response = requests.get(url, timeout=10)
        
        # response.content returnează textul sub formă de byți (necesar pentru hashlib)
        # hexdigest() transformă rezultatul într-un șir de caractere citibil (hexazecimal)
        amprenta = hashlib.sha256(response.content).hexdigest()
        
        return amprenta
        
    except requests.RequestException:
        return None

# --- Testarea funcției ---
BASE_URL = "https://cybercor.org"

# Rulăm funcția de două ori
amprenta_1 = page_fingerprint(BASE_URL)
amprenta_2 = page_fingerprint(BASE_URL)

print(f"Prima amprentă:  {amprenta_1}")
print(f"A doua amprentă: {amprenta_2}")

# Comparam rezultatele
if amprenta_1 == amprenta_2:
    print("\nRezultat: Amprentele sunt IDENTICE.")
else:
    print("\nRezultat: Amprentele sunt DIFERITE.")



# Laborator: Salvarea în JSON 

# Student: <Grecu Gabriela> 

import requests
import json

BASE_URL = "https://cybercor.org"

try:
    # 1. Facem cererea pentru a obține antetele paginii principale
    response = requests.get(BASE_URL, timeout=10)
    
    # Transformăm structura de antete a requests într-un dicționar clasic Python
    antete_dict = dict(response.headers)
    
    # 2. SALVAREA ÎN JSON
    # Deschidem un fișier numit 'headers.json' în modul "w" (write/scriere)
    with open("headers.json", "w") as file:
        # json.dump scrie dicționarul în fișier.
        # indent=2 adaugă spații și rânduri noi ca fișierul să fie ușor de citit de om
        json.dump(antete_dict, file, indent=2)
        
    print("Antetele au fost salvate cu succes în 'headers.json'.")

    # 3. ÎNCĂRCAREA DIN JSON
    # Deschidem fișierul proaspăt creat în modul "r" (read/citire)
    with open("headers.json", "r") as file:
        # json.load citește textul din fișier și îl transformă la loc într-un dicționar Python
        antete_incarcate = json.load(file)
        
    # 4. AFIȘAREA UNUI ANTET
    # Extragem un antet specific, de exemplu 'Content-Type' sau 'Server'
    antet_cautat = antete_incarcate.get("Content-Type", "Antetul nu a fost găsit")
    
    print("\nDate încărcate din fișier:")
    print(f"Content-Type: {antet_cautat}")

except requests.RequestException:
    print("Eroare: Nu am putut accesa site-ul pentru a obține antetele.")



# Laborator: Interogare DNS. 

# Student: <Grecu Gabriela> 

import socket

def resolve(hostname):
    """
    Primește un nume de domeniu (fără https://) și 
    returnează adresa sa IP folosind o interogare DNS.
    """
    try:
        # gethostbyname face conversia din nume (ex: cybercor.org) în IP
        adresa_ip = socket.gethostbyname(hostname)
        return adresa_ip
        
    except socket.gaierror:
        # gaierror (Get Address Info Error) apare dacă domeniul nu există
        return "Domeniul nu a putut fi găsit (DNS Error)"

# --- Testarea funcției ---
# Atenție: Interogarea DNS se face doar pe numele domeniului, 
# deci NU punem "https://" sau "/path" la început.
domeniu = "cybercor.org"

rezultat_ip = resolve(domeniu)
print(f"Adresa IP a domeniului {domeniu} este: {rezultat_ip}")


# Laborator: Expirarea certificatului.

# Student: <Grecu Gabriela> 

import socket
import ssl
import time

def cert_days_left(hostname):
    """
    Se conectează la portul 443 (HTTPS), obține certificatul
    și returnează câte zile mai sunt până la expirarea acestuia.
    """
    # 1. Creăm contextul SSL conform indiciului
    context = ssl.create_default_context()
    
    try:
        # 2. Creăm conexiunea de rețea de bază
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            
            # 3. Încapsulăm conexiunea în SSL (tunel criptat)
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                
                # 4. Obținem certificatul și extragem data expirării
                certificat = ssock.getpeercert()
                data_text = certificat["notAfter"]
                
                # 5. Convertim data expirării în secunde
                expirare_secunde = ssl.cert_time_to_seconds(data_text)
                
                # 6. Calculăm diferența de timp
                timp_curent_secunde = time.time()
                secunde_ramase = expirare_secunde - timp_curent_secunde
                
                # Transformăm secundele în zile (24 ore * 3600 secunde)
                zile_ramase = int(secunde_ramase / 86400)
                
                return zile_ramase
                
    except Exception as e:
        print(f"A apărut o eroare: {e}")
        return None

# --- Testarea funcției ---
domeniu = "cybercor.org"
zile = cert_days_left(domeniu)

if zile is not None:
    print(f"Certificatul pentru {domeniu} mai este valabil {zile} zile.")




    #verificare: Clasa HTMLParser o apelează automat. Când folosești comanda finder.feed(text), parserul citește tot codul HTML din spate. Imediat ce dă de un tag (cum ar fi <img>), el declanșează singur metoda handle_starttag() pentru acel tag. Tu doar îi dai textul paginii, iar sistemul face automat apelurile în fundal.
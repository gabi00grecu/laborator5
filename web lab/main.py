# Laborator: Importarea unui nou modul

# Student: <Grecu Gabriela> 

  

BASE_URL = "https://cybercor.org" 

ECHO_URL = "https://httpbin.org" 

TIMEOUT = 10  # secunde 
import webtools

# Apelăm funcțiile folosind prefixul "webtools." exact cum cere exercițiul
titlu = webtools.get_title(webtools.fetch(BASE_URL).text)

print(f"Titlul extras prin modulul webtools este: {titlu}")




# Laborator:  Importarea anumitor nume.

# Student: <Grecu Gabriela> 

# Modificăm importul general într-unul specific
from webtools import get_title, security_headers, fetch


# Acum apelăm funcțiile direct, fără a mai pune "webtools." în fața lor
html_text = fetch(BASE_URL).text
titlu = get_title(html_text)

print(f"Titlul paginii este: {titlu}")

"""
Explicație pentru Exercițiul 45:
Dacă main.py ar avea propria funcție numită `get_title`, ar avea loc un conflict de nume (Name Collision).
Concret, ultima funcție definită sau importată ar "câștiga". 
Dacă definești funcția ta `get_title` DUPĂ acest import, ea va suprascrie/șterge din memorie funcția adusă din webtools. Dacă o definești ÎNAINTE de import, importul o va suprascrie pe a ta.
Din acest motiv, când importăm funcții specifice cu `from ... import`, trebuie să fim atenți să nu folosim aceleași nume în programul nostru principal.
"""





# Laborator: Constante de modul

# Student: <Grecu Gabriela> 

# Importăm constanta alături de celelalte funcții necesare
from webtools import DEFAULT_HEADERS, get_title, fetch

BASE_URL = "https://cybercor.org"

# Afișăm constanta așa cum cere cerința
print(f"Constanta DEFAULT_HEADERS importată: {DEFAULT_HEADERS}")

# Continuăm cu apelurile obișnuite
html_text = fetch(BASE_URL).text
titlu = get_title(html_text)
print(f"Titlul paginii: {titlu}")




# Laborator: Argumente din linia de comanda

# Student: <Grecu Gabriela> 


import argparse
from webtools import DEFAULT_HEADERS, get_title, fetch

# 1. Configurarea parserului pentru linia de comandă
parser = argparse.ArgumentParser(description="Script de analiză web folosind webtools.")
parser.add_argument("url", help="URL-ul complet al site-ului pe care dorești să îl analizezi")

# 2. Citirea argumentelor trimise de utilizator
args = parser.parse_args()

# Afișăm constanta de la exercițiul anterior
print(f"Constanta DEFAULT_HEADERS: {DEFAULT_HEADERS}")
print(f"Se analizează adresa: {args.url}\n")

# 3. Transmitem argumentul URL funcțiilor, în loc să folosim BASE_URL
try:
    # Apelăm funcția fetch folosind arg.url
    raspuns = fetch(args.url)
    titlu = get_title(raspuns.text)
    
    print(f"Titlul paginii obținute: {titlu}")

except Exception as e:
    print(f"Eroare la accesarea adresei: {e}")



# Laborator: Raport CSV

# Student: <Grecu Gabriela> 

import argparse
import csv
from datetime import datetime
from webtools import check_paths

# Preluăm URL-ul din linia de comandă (Exercițiul 48)
parser = argparse.ArgumentParser(description="Raport CSV")
parser.add_argument("url", help="URL-ul site-ului")
args = parser.parse_args()

# Căile de verificat pe site
cai_de_verificat = ["/", "/robots.txt", "/sitemap.xml", "/admin"]

print(f"Se verifică rutele pentru: {args.url} ...")
rezultate_cai = check_paths(args.url, cai_de_verificat)

# Salvăm rezultatul în report.csv conform Exercițiului 49
with open("report.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # Scriem antetul cu exact coloanele cerute
    writer.writerow(["path", "status", "checked_at"])
    
    # Obținem ora curentă în formatul isoformat()
    timp_curent = datetime.now().isoformat()
    
    # Scriem rândurile pentru fiecare cale verificată
    for cale, status in rezultate_cai.items():
        writer.writerow([cale, status, timp_curent])

print("Fișierul 'report.csv' a fost generat cu succes!")




# Laborator: Proiect final: raportul site-ului

# Student: <Grecu Gabriela>


import argparse
from webtools import site_report

# Preluăm URL-ul din linia de comandă (Exercițiul 48)
parser = argparse.ArgumentParser(description="Raport final site web")
parser.add_argument("url", help="URL-ul complet al site-ului (ex: https://cybercor.org)")
args = parser.parse_args()

# Apelăm proiectul final (Exercițiul 50) care afișează raportul și generează report.json
site_report(args.url)





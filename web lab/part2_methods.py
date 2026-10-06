# Laborator: Elementele de bază ale răspunsului

# Student: <Grecu Gabriela> 

  

BASE_URL = "https://cybercor.org" 

ECHO_URL = "https://httpbin.org" 

TIMEOUT = 10  # secunde 

# Laborator: Elementele de bază ale răspunsului

# Student: <Grecu Gabriela> 
import requests
requests.get(BASE_URL, timeout = TIMEOUT)
response = requests.get(BASE_URL)
print(response.status_code)
print(response.ok)
print(response.url)
print(response.encoding)
#toate 4 sunt atribute, deoarece nu se termina in ()

# Laborator: Tratarea erorilor cu o metodă.

# Student: <Grecu Gabriela> 
response = requests.get(BASE_URL, timeout=TIMEOUT)
response.raise_for_status()

# 2. Trimitem cererea către pagina inexistentă și prindem excepția
try:
    response = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    response.raise_for_status()
except requests.exceptions.HTTPError:
    print("Pagina nu există! Verifică linkul introdus.")


# Laborator: Toate antetele.
# Student: <Grecu Gabriela> 
response = requests.get(BASE_URL, timeout = TIMEOUT)
# Parcurgem dicționarul de antete folosind .items()
for nume, valoare in response.headers.items():
    # Afișăm în formatul cerut folosind f-strings
    print(f"{nume}: {valoare}")
# Laborator:  Metode de dicționar.

# Student: <Grecu Gabriela> 
response = requests.get(BASE_URL, timeout = TIMEOUT)
# Afișăm antetele 'Server' și 'Content-Type', folosind "lipsește" ca valoare implicită
antet_server = response.headers.get("Server", "lipsește")
antet_content_type = response.headers.get("Content-Type", "lipsește")

print(f"Server: {antet_server}")
print(f"Content-Type: {antet_content_type}")

# Încercăm cu litere mici, conform cerinței
antet_litere_mici = response.headers.get("content-type", "lipsește")
print(f"content-type (litere mici): {antet_litere_mici}")
#Ambele variante pentru "Content-Type" (și cea cu litere mari, și cea cu litere mici) returnează exact aceeași valoare.


# Laborator: Inlănțuirea metodelor de șir

# Student: <Grecu Gabriela> 
response = requests.get(BASE_URL, timeout = TIMEOUT)
numar_aparitii = response.text.lower().count("cyber")
print(f"Cuvantul 'cyber'' apare de {numar_aparitii} ori pe pagina")

# Laborator:  Găsirea titlului

# Student: <Grecu Gabriela> 
response = requests.get(BASE_URL, timeout = TIMEOUT)
html = response.text
start = html.find('<title>') + len ('<title>')
end = html.find('</title>')
titlu_curat = html[start:end].strip()

print(titlu_curat)
# Laborator: Numărarea liniilor.

# Student: <Grecu Gabriela> 
response = requests.get(BASE_URL, timeout = TIMEOUT)
linii = response.text.splitlines()
numar_linii = len(linii)
longest_line = max(linii, key=len)
print(f"Numarul de linii este {numar_linii} si cea mai lunga este {longest_line}")


# Laborator: Verificarea HTTPS.

# Student: <Grecu Gabriela> 
response = requests.get(BASE_URL, timeout = TIMEOUT)
if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")

# Laborator: Urmărirea redirecționărilor

# Student: <Grecu Gabriela> 
response = requests.get(BASE_URL, timeout = TIMEOUT)
response = requests.get("http://cybercor.org")

for redirect in response.history:
    # Apasă tasta TAB la începutul acestui rând:
    print(f"Status: {redirect.status_code} | URL: {redirect.url}")

print(f"URL final: {response.url}")


# Laborator: HEAD versus GET. 

# Student: <Grecu Gabriela> 
# 1. Trimitem cererea cu HEAD
response_head = requests.head(BASE_URL)

# 2. Trimitem cererea cu GET
response_get = requests.get(BASE_URL)

# 3. Afișăm și comparăm lungimea conținutului
print(f"Lungime HEAD: {len(response_head.content)} octeți")
print(f"Lungime GET: {len(response_get.content)} octeți")
# Explicația diferenței:
# O cerere GET cere serverului să trimită totul: și antetele (metadatele), și corpul paginii (tot codul HTML). De aceea lungimea sa este mare.
# O cerere HEAD cere serverului SĂ TRIMITĂ DOAR ANTETELE, fără să descarce corpul paginii. 
# Prin urmare, len(response_head.content) va fi întotdeauna 0. Această metodă este foarte rapidă și utilă dacă vrem doar să verificăm dacă o pagină există (status code) sau cât de mare este un fișier, fără să consumăm trafic pentru a-l descărca


# Laborator: Cookie-uri.

# Student: <Grecu Gabriela> 
import requests

# (Presupunem că BASE_URL este definit și ai făcut deja cererea)
# response = requests.get(BASE_URL)

# Verificăm dacă există cel puțin un cookie în răspuns
if len(response.cookies) == 0:
    print("Niciun cookie setat.")
else:
    # Dacă există, parcurgem lista de cookie-uri
    for cookie in response.cookies:
        print(f"Nume: {cookie.name}, Securizat: {cookie.secure}")



# Laborator: Sesiuni

# Student: <Grecu Gabriela> 

import requests

# (Presupunem că ECHO_URL este definit mai sus, de ex: ECHO_URL = "https://httpbin.org")

# 1. Creăm obiectul Session
session = requests.Session()

# 2. Setăm User-Agent-ul personalizat
session.headers.update({"User-Agent": "WebLab-Grecu Gabriela"})

# 3. Trimitem cererea folosind obiectul 'session' (nu 'requests')
response = session.get(ECHO_URL + "/headers")

# 4. Afișăm răspunsul primit de la server pentru a confirma că antetul a fost trimis
print("Corpul răspunsului:")
print(response.text)

#response.text este un atribut (o proprietate). Funcționează ca o variabilă internă a obiectului response care stochează pur și simplu textul brut primit de la server. Pentru a citi o valoare stocată, nu ai nevoie de paranteze.
#response.json() este o metodă (o funcție internă). Aceasta nu stochează doar o valoare gata făcută, ci execută o acțiune: ia textul brut, îl analizează (parsează) și îl convertește într-un format pe care Python îl înțelege mai ușor (de obicei un dicționar sau o listă). Deoarece este o funcție care trebuie executată pentru a-ți da rezultatul, are nevoie de paranteze () pentru a fi apelată.
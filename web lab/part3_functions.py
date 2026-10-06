# Laborator: Prima funcție 
# Student: <Grecu Gabriela> 

  

BASE_URL = "https://cybercor.org" 

ECHO_URL = "https://httpbin.org" 

TIMEOUT = 10  # secunde 

import requests
def fetch(url):
    """Returnează întregul obiect răspuns pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response

# Apelăm funcția pentru BASE_URL și salvăm rezultatul
rezultat = fetch(BASE_URL)

# Deoarece funcția noastră returnează obiectul complet (și nu doar un număr),
# putem extrage statusul sau orice alt atribut din el aici, în afara funcției:
print(f"Codul de stare este: {rezultat.status_code}")


# Laborator: Returnarea unei singure valori 
# Student: <Grecu Gabriela> 
import time
def get_status(url):
    """Returnează doar codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

# Definim căile pe care vrem să le verificăm
cai_de_verificat = ["/", "/robots.txt", "/sitemap.xml"]

# Parcurgem fiecare cale
for cale in cai_de_verificat:
    url_complet = BASE_URL + cale
    
    # Apelăm funcția noastră pentru a obține statusul
    status = get_status(url_complet)
    print(f"URL: {url_complet} | Status: {status}")
    
    # Facem o pauză de 1 secundă înainte de următoarea cerere
    time.sleep(1)



# Laborator: Parametri impliciți.  
# Student: <Grecu Gabriela> 

# Modificăm funcția pentru a accepta 'timeout' cu o valoare implicită de 10
def fetch(url, timeout=10):
    """Returnează obiectul răspuns, folosind un timeout implicit de 10 secunde."""
    response = requests.get(url, timeout=timeout)
    return response

# 1. Apelăm funcția folosind valoarea implicită (nu specificăm timeout-ul)
# Va folosi automat timeout=10
rezultat_implicit = fetch(BASE_URL)
print(f"Apel 1 (implicit): Status {rezultat_implicit.status_code}")

# 2. Apelăm funcția suprascriind valoarea implicită cu timeout=3
# Va ignora valoarea de 10 și va folosi 3
rezultat_rapid = fetch(BASE_URL, timeout=3)
print(f"Apel 2 (timeout=3): Status {rezultat_rapid.status_code}")




# Laborator: O singură sarcină pe funcție
# Student: <Grecu Gabriela> 

def get_title(html):
    # 1. Găsim punctul de start (imediat după eticheta <title>)
    start = html.find("<title>") + len("<title>")
    
    # 2. Găsim punctul de final (începutul etichetei </title>)
    end = html.find("</title>")
    
    # 3. Extragem porțiunea de text și o curățăm cu .strip()
    titlu = html[start:end].strip()
    
    # 4. Returnăm rezultatul
    return titlu



# Laborator: Docstring-uri 
# Student: <Grecu Gabriela> 

def get_title(html):
    
   # Extrage și returnează textul curățat dintre etichetele <title> și </title> dintr-un cod HTML furnizat ca șir de caractere (string).
    
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    return html[start:end].strip()

# Apelăm funcția help() pentru a afișa documentația pe care tocmai am scris-o
help(get_title)


# Laborator:  Adnotări de tip
# Student: <Grecu Gabriela> 

TIMEOUT = 10

# Am adăugat adnotările de tip: url trebuie să fie 'str' (string), iar funcția returnează 'int' (întreg)
def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code


# Laborator: Fără opriri neașteptate
# Student: <Grecu Gabriela> 

def page_exists(url):
    # 'try' este decalat cu un Tab față de 'def'
    try:
        # 'requests.get' este decalat cu încă un Tab față de 'try'
        requests.get(url, timeout=10)
        return True
        
    # 'except' trebuie să fie la același nivel cu 'try'
    except requests.RequestException:
        # 'return' este decalat cu un Tab față de 'except'
        return False

# Aici ieșim din funcție, deci codul revine la marginea din stânga
rezultat = page_exists("https://this-domain-does-not-exist.invalid")
print(f"Pagina există? {rezultat}")


# Laborator: Returnarea unui dicționar
# Student: <Grecu Gabriela> 

def check_paths(base, paths):

    # 1. Creăm un dicționar gol pentru a stoca rezultatele
    dictionar_status = {}
    
    # 2. Parcurgem fiecare cale din lista primită
    for path in paths:
        # Construim adresa completă (ex: "http://cybercor.org" + "/robots.txt")
        url_complet = base + path
        
        # Facem cererea web
        response = requests.get(url_complet, timeout=10)
        
        # 3. Adăugăm o intrare nouă în dicționar
        # Cheia va fi calea (path), iar valoarea va fi statusul (status_code)
        dictionar_status[path] = response.status_code
        
    # 4. După ce bucla s-a terminat, returnăm dicționarul complet
    return dictionar_status

cai_de_verificat = ["/", "/robots.txt", "/sitemap.xml"]

# Apelăm funcția și salvăm dicționarul returnat
rezultate = check_paths(BASE_URL, cai_de_verificat)

# Afișăm dicționarul final
print(rezultate)



# Laborator: Argumente cu nume.
# Student: <Grecu Gabriela> 
# 1. Definim funcția care primește cei 3 parametri
def get_header(url, name, default="lipsește"):
    # Facem cererea către pagina web
    response = requests.get(url, timeout=10)
    
    # Extragem antetul cerut folosind metoda .get() a dicționarului de antete
    # Această metodă folosește automat 'default' dacă antetul nu există
    valoare_antet = response.headers.get(name, default)
    
    return valoare_antet

# 2. Apelăm funcția folosind argumente cu nume (keyword arguments), exact cum cere exercițiul

rezultat = get_header(url=BASE_URL, name="Server")
print(f"Antetul Server este: {rezultat}")


# Laborator: Antete de securitate 
# Student: <Grecu Gabriela> 

def security_headers(url):
   
    # Lista cu antetele pe care vrem să le căutăm
    antete_de_cautat = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    
    rezultate = {}
    
    try:
        # Facem cererea către URL
        response = requests.get(url, timeout=10)
        
        # Parcurgem lista noastră de antete
        for antet in antete_de_cautat:
            # Verificăm dacă antetul există în răspunsul primit de la server
            # 'antet in response.headers' va returna automat True sau False
            rezultate[antet] = antet in response.headers
            
    except requests.RequestException:
        # Dacă site-ul nu funcționează, setăm automat False pentru toate
        for antet in antete_de_cautat:
            rezultate[antet] = False
            
    return rezultate



# Laborator: Funcții care apelează funcții 
# Student: <Grecu Gabriela> 


# (Funcția de la Exercițiul 30)
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

# (Funcția nouă pentru Exercițiul 31)
def score_headers(results):
  
    # Calculăm numărul total de antete verificate (lungimea dicționarului)
    total = len(results)
    
    # În Python, True are valoarea matematică 1, iar False are valoarea 0.
    # Putem folosi sum() pe valorile dicționarului pentru a aduna toți de True.
    scor = sum(results.values())
    
    # Returnăm rezultatul formatat ca șir de caractere (string)
    return f"{scor}/{total}"

# Apelăm funcția score_headers și îi dăm ca argument direct REZULTATUL funcției security_headers

rezultat_final = score_headers(security_headers(BASE_URL))

print(f"Scorul antetelor de securitate este: {rezultat_final}")

# Laborator: Două funcții, o sarcină 
# Student: <Grecu Gabriela> 

def fetch_robots(base):
    
    url = base + "/robots.txt"
    try:
        response = requests.get(url, timeout=10)
        # Ne asigurăm că pagina chiar există (codul 200 OK)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.RequestException:
        # Dacă pică internetul sau domeniul nu există, returnăm tot None
        return None

def disallowed_paths(robots_text):
 
    # 1. Tratăm cazul în care textul lipsește (fetch_robots a returnat None)
    if robots_text is None:
        return []
    
    cai_interzise = []
    
    # 2. Împărțim textul pe rânduri folosind .splitlines() (învățat la Ex 15)
    for line in robots_text.splitlines():
        # Curățăm rândul de spații și verificăm dacă începe cu "Disallow:"
        if line.strip().startswith("Disallow:"):
            # Împărțim rândul în două bucăți la cuvântul "Disallow:"
            # A doua bucată (indexul 1) va fi calea efectivă.
            cale = line.split("Disallow:")[1].strip()
            cai_interzise.append(cale)
            
    return cai_interzise

# Pasul 1: Aducem textul
text_robots = fetch_robots(BASE_URL)

# Pasul 2: Extragem căile
lista_disallow = disallowed_paths(text_robots)

print(f"Am găsit {len(lista_disallow)} căi interzise:")
print(lista_disallow)



# Laborator:  Oricâte argumente. 
# Student: <Grecu Gabriela> 

import requests

def response_times(*urls):
   
    timpi_raspuns = {}
    
    # 'urls' se comportă acum ca o listă cu toate argumentele primite
    for url in urls:
        try:
            # Facem cererea web
            response = requests.get(url, timeout=10)
            
            # '.elapsed' este un obiect care măsoară timpul trecut.
            # Metoda '.total_seconds()' ne dă direct valoarea în secunde.
            timp = response.elapsed.total_seconds()
            
            # Adăugăm în dicționar
            timpi_raspuns[url] = timp
            
        except requests.RequestException:
            # Dacă site-ul nu merge, punem valoarea None ca măsură de siguranță
            timpi_raspuns[url] = None
            
    return timpi_raspuns


rezultate = response_times("http://cybercor.org", "https://google.com")

print(rezultate)


# Laborator: Argumente cu nume colectate.  
# Student: <Grecu Gabriela> 

def log(message, **details):
   
    # Începem prin a transforma mesajul principal într-o listă care conține doar acest mesaj
    elemente = [str(message)]
    
    # Parcurgem dicționarul generat de **details
    for cheie, valoare in details.items():
        # Adăugăm fiecare pereche formatată în lista noastră
        elemente.append(f"{cheie}={valoare}")
        
    # Unim toate elementele din listă punând " | " între ele
    rezultat_final = " | ".join(elemente)
    
    print(rezultat_final)


# Apelăm funcția exact ca în exemplu
log("verificat", url=BASE_URL, status=200)

#Diferenta dintre print() si return: Print este pentru persoana care citeste codul. Are functia de a afisa un text care nu afecteaza programul cu nimic. Return este pentru program si indica ce valoare trebuie sa iasa din indeplinirea unei conditii/functii
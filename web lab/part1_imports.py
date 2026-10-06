# Laborator: funcții, metode și importuri pe web 
# Student: <Grecu Gabriela> 

  

BASE_URL = "https://cybercor.org" 

ECHO_URL = "https://httpbin.org" 

TIMEOUT = 10  # secunde
import requests #modulul Requests necesita pip install deoarece este o biblioteca externa care vine impachetata cu python
print (requests.__version__)
import urllib.request #modulul urllib nu necesita pip install deoarece este o biblioteca interna care vine impachetata cu python
requests.get (BASE_URL)

# Laborator: Doua stiluri de import
# Student: <Grecu Gabriela> 

response1 = requests.get(BASE_URL, timeout = TIMEOUT) #codul este mai clar si se intelege din ce biblioteca e functia get()
print("Stilul 1 - starea codului: ", response1.status_code)
from requests import get
response2 = get(BASE_URL, timeout = TIMEOUT) #codul devine mai concis la apelare get () dar nu request.get ()
print("Stilul 2 - starea codului: ", response2.status_code)

# Laborator: Alias-uri
# Student: <Grecu Gabriela> 
import requests as rq
response3 = rq.get(BASE_URL, timeout = TIMEOUT)
print("Stilul 3 - starea codului: ", response3.status_code)

# Laborator: Doar biblioteca standard
# Student: <Grecu Gabriela>
import urllib.request

# Definim un User-Agent de browser pentru a nu fi blocați cu eroarea 403
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Creăm un obiect Request care include adresa și headerele de browser
req = urllib.request.Request(BASE_URL, headers=headers)

# Trimitem cererea folosind obiectul Request configurat
with urllib.request.urlopen(req) as response:
    status_code = response.status
    raw_body = response.read()
    text_body = raw_body.decode("utf-8")

    print(f"Status: {status_code}")
    print(text_body[:200])

# Laborator: interiorul unui modul
# Student: <Grecu Gabriela>
print(dir(requests))
# Salvăm rezultatul într-o variabilă, apoi alegem primele 3 elemente
toate_atributele = dir(requests)
# Alegem primele 3 elemente din listă folosind felierea (slicing)
primele_trei = toate_atributele[:3]
print(primele_trei)
#ConnectTimeout si ConnectionError sunt clase de erori, iar DependencyWarning este o clasa de avertisment

# Laborator: Citim documentatia
# Student: <Grecu Gabriela>
help(requests.get)
# Trimitem o cerere GET folosind parametrul timeout setat la 10 secunde
response = requests.get(BASE_URL, timeout=10)

# Afișăm codul de stare HTTP al răspunsului
print(f"Status: {response.status_code}")

# Afișăm primele 200 de caractere din corpul răspunsului folosind felierea (slicing)
print(response.text[:200])

# Laborator: Cronometrarea unei cereri
# Student: <Grecu Gabriela>
import time

# Salvăm momentul de timp exact înainte de lansarea cererii folosind time.perf_counter()
start_time = time.perf_counter()

# Trimitem cererea GET către pagina principală
response = requests.get(BASE_URL, timeout=10)

# Salvăm momentul de timp imediat după ce am primit răspunsul complet
end_time = time.perf_counter()

# Calculăm durata totală scursă măsurată manual cu modulul time
durata_time = end_time - start_time

# Afișăm rezultatul măsurat manual și cel oferit nativ de obiectul response
print(f"Timp măsurat cu time.perf_counter(): {durata_time:.6f} secunde")
print(f"Timp măsurat de biblioteca requests (response.elapsed): {response.elapsed.total_seconds()} secunde")

# Laborator: Importul esueaza
#Student: <Grecu Gabriela>
requests.get(BASE_URL, timeout = TIMEOUT)
try:
    import bs4
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")
# Modul: Un singur fișier Python (.py).
# Pachet: Un folder care conține mai multe module.
# Bibliotecă: O colecție amplă de pachete și module gata de folosit (ex: requests, urllib).

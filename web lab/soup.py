from bs4 import BeautifulSoup

def get_title(html):
    """Extrage titlul paginii folosind BeautifulSoup (scurt și sigur)."""
    soup = BeautifulSoup(html, 'html.parser')
    title_tag = soup.find('title')
    return title_tag.text.strip() if title_tag else "N/A"

def extract_links(html):
    """Extrage toate linkurile href folosind BeautifulSoup."""
    soup = BeautifulSoup(html, 'html.parser')
    return [a.get('href') for a in soup.find_all('a', href=True)]

    #Cu RegEx (re): Codul era fragil. O singură literă mare (de ex. <TITLE>), un spațiu în plus (<title >) sau un tag întrerupt putea strica complet căutarea și returna erori, necesitând expresii regulate complicate și greu de întreținut.
    #Cu BeautifulSoup (bs4): Codul devine mult mai scurt (de la șiruri lungi de regex la o singură linie precum soup.find('title')), iar biblioteca se ocupă automat de interpretarea corectă a oricărui tip de HTML, fiind mult mai sigură și robust
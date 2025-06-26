import re
import ipaddress
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import socket

def having_ip_address(url):
    domain = urlparse(url).netloc
    try:
        ipaddress.ip_address(domain)
        return 1
    except ValueError:
        return -1

def url_length(url):
    length = len(url)
    if length < 54:
        return -1
    elif length <= 75:
        return 0
    else:
        return 1

def shortening_service(url):
    shortening_services = r"(bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co|is\.gd|buff\.ly|adf\.ly|bitly\.com|tinyurl\.com)"
    if re.search(shortening_services, url):
        return 1
    else:
        return -1

def having_at_symbol(url):
    return 1 if '@' in url else -1

def double_slash_redirecting(url):
    pos = url.find('//', url.find('://') + 3)
    return 1 if pos != -1 else -1

def prefix_suffix(url):
    domain = urlparse(url).netloc
    return 1 if '-' in domain else -1

def having_sub_domain(url):
    domain = urlparse(url).netloc
    if domain.count('.') == 1:
        return -1
    elif domain.count('.') == 2:
        return 0
    else:
        return 1

def ssl_final_state(url):
    try:
        if not url.startswith("https://"):
            return 1
        response = requests.get(url, timeout=5)
        if response.url.startswith("https://"):
            return -1
        else:
            return 1
    except:
        return 1

def domain_registration_length(url):
    # À améliorer avec un vrai WHOIS
    # Ici on renvoie -1 par défaut
    return -1

def favicon(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        icon_link = soup.find("link", rel=lambda x: x and 'icon' in x.lower())
        if icon_link:
            href = icon_link.get('href')
            href_domain = urlparse(href).netloc
            url_domain = urlparse(url).netloc
            if href_domain == "" or href_domain == url_domain:
                return -1
            else:
                return 1
        else:
            return 1
    except:
        return 1

def port(url):
    domain = urlparse(url).netloc
    if ':' in domain:
        port = domain.split(':')[1]
        if port not in ['80', '443']:
            return 1
        else:
            return -1
    else:
        return -1

def https_token(url):
    domain = urlparse(url).netloc
    return 1 if 'https' in domain else -1

def request_url(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup.find_all(['img', 'script', 'iframe']):
            src = tag.get('src')
            if src:
                if urlparse(src).netloc != "" and urlparse(src).netloc != urlparse(url).netloc:
                    return 1
        return -1
    except:
        return 1

def url_of_anchor(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        total = 0
        suspicious = 0
        for a in soup.find_all('a', href=True):
            total += 1
            href = a['href']
            if href.startswith('#') or href.lower().startswith('javascript:void(0)') or urlparse(href).netloc != urlparse(url).netloc:
                suspicious += 1
        if total == 0:
            return -1
        ratio = suspicious / total
        if ratio < 0.31:
            return -1
        elif ratio <= 0.67:
            return 0
        else:
            return 1
    except:
        return 1

def links_in_tags(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        total = 0
        suspicious = 0
        tags = ['link', 'script', 'meta']
        for tag in tags:
            for t in soup.find_all(tag):
                total += 1
                href = t.get('href') or t.get('src') or ''
                if href != '' and urlparse(href).netloc != '' and urlparse(href).netloc != urlparse(url).netloc:
                    suspicious += 1
        if total == 0:
            return -1
        ratio = suspicious / total
        if ratio < 0.17:
            return -1
        elif ratio <= 0.81:
            return 0
        else:
            return 1
    except:
        return 1

def sfh(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action')
            if action is None or action == "" or action == "about:blank":
                return 1
            elif urlparse(action).netloc != "" and urlparse(action).netloc != urlparse(url).netloc:
                return 1
        return -1
    except:
        return 1

def submitting_to_email(url):
    try:
        response = requests.get(url, timeout=5)
        if re.search(r"mailto:", response.text):
            return 1
        else:
            return -1
    except:
        return 1

def abnormal_url(url):
    # Normalement, besoin d’un check WHOIS ou certificat SSL correct
    return -1

def redirect(url):
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        if len(response.history) > 1:
            return 1
        else:
            return -1
    except:
        return 1

def on_mouseover(url):
    try:
        response = requests.get(url, timeout=5)
        if "onmouseover" in response.text.lower():
            return 1
        else:
            return -1
    except:
        return 1

def right_click(url):
    try:
        response = requests.get(url, timeout=5)
        if "event.button==2" in response.text:
            return 1
        else:
            return -1
    except:
        return 1

def popup_window(url):
    try:
        response = requests.get(url, timeout=5)
        if "popup" in response.text.lower():
            return 1
        else:
            return -1
    except:
        return 1

def iframe(url):
    try:
        response = requests.get(url, timeout=5)
        if "<iframe" in response.text.lower():
            return 1
        else:
            return -1
    except:
        return 1

def age_of_domain(url):
    # Placeholder : besoin WHOIS lookup pour date de création du domaine
    return -1

def dns_record(url):
    domain = urlparse(url).netloc
    try:
        socket.gethostbyname(domain)
        return -1
    except:
        return 1

def web_traffic(url):
    # Besoin API Alexa ou autre — on met -1 par défaut
    return -1

def page_rank(url):
    # Besoin API Google PageRank (indisponible) — on met -1 par défaut
    return -1

def google_index(url):
    # Impossible sans scraping Google, on met -1 par défaut
    return -1

def links_pointing_to_page(url):
    # Besoin API externe, on met -1 par défaut
    return -1

def statistical_report(url):
    # Besoin base de données ou service externe, on met -1 par défaut
    return -1

def extract_features(url):
    features = []
    features.append(having_ip_address(url))
    features.append(url_length(url))
    features.append(shortening_service(url))
    features.append(having_at_symbol(url))
    features.append(double_slash_redirecting(url))
    features.append(prefix_suffix(url))
    features.append(having_sub_domain(url))
    features.append(ssl_final_state(url))
    features.append(domain_registration_length(url))
    features.append(favicon(url))
    features.append(port(url))
    features.append(https_token(url))
    features.append(request_url(url))
    features.append(url_of_anchor(url))
    features.append(links_in_tags(url))
    features.append(sfh(url))
    features.append(submitting_to_email(url))
    features.append(abnormal_url(url))
    features.append(redirect(url))
    features.append(on_mouseover(url))
    features.append(right_click(url))
    features.append(popup_window(url))
    features.append(iframe(url))
    features.append(age_of_domain(url))
    features.append(dns_record(url))
    features.append(web_traffic(url))
    features.append(page_rank(url))
    features.append(google_index(url))
    features.append(links_pointing_to_page(url))
    features.append(statistical_report(url))
    return features


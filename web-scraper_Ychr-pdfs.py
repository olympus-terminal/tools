import os
import requests
import pdfplumber
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def download_pdf_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    urls = []
    for link in soup.select("a[href$='.pdf']"):
        url = link['href']
        if is_valid(url):
            urls.append(url)
    return urls

def download_pdf(url, dirname):
    response = requests.get(url)
    filename = os.path.join(dirname, url.split("/")[-1])

    with open(filename, 'wb') as out_file:
        out_file.write(response.content)
        
def convert_pdf_to_txt(path):
    txt_path = path.replace('.pdf', '.txt')
    with pdfplumber.open(path) as pdf:
        text = '\n'.join(page.extract_text() for page in pdf.pages)
    
    with open(txt_path, 'w') as f:
        f.write(text)
        
# Enter the directory where you want to put manuscripts
dir_name = 'manuscripts'
os.makedirs(dir_name, exist_ok=True)

# Loop all pages you want to check
for i in range(1, 101):
    url = f"https://www.biorxiv.org/search/Y%20chromosome%20numresults%3A75%20sort%3Arelevance-rank%20format_result%3Astandard?page={i}"
    pdf_urls = download_pdf_urls(url)

    for pdf_url in pdf_urls:
        download_pdf(pdf_url, dir_name)
        convert_pdf_to_txt(os.path.join(dir_name, pdf_url.split("/")[-1]))

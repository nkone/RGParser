import requests
from bs4 import BeautifulSoup

url = "http://192.168.1.254/xslt?PAGE=C_0_0"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
    'Content-Type': 'text/html',
}

response = requests.get(url, headers=headers)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

a_string = soup.find_all("td",string="Model")[0]

print(a_string)
print(a_string.find_next_sibling("td").string)


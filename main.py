import requests

from bs4 import BeautifulSoup

main_url = "http://books.toscrape.com/index.html"

result = requests.get(main_url)

print(result.text[:1000])



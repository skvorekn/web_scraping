import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

main_url = "http://books.toscrape.com/index.html"

def getAndParseURL(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return(soup)

# find the URL of every book product page
# by inspecting the book links for every product, the HTML structure is always the same
# corresponds to href attribute of the a tag
# article tag with the class value of product_pod

def getBooksURLs(url):
    soup = getAndParseURL(url)
    return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.findAll("article",
                                                                                            class_ = "product_pod")])
print("First book URL:")
print(getBooksURLs(main_url)[0])

# find book categories URLs on the main page
# URL pattern is catalogue/category/books
soup = getAndParseURL(main_url)
categories_urls = ["/".join(main_url.split("/")[:-1]) + "/" + x.get('href') for x in soup.findAll("a", href=re.compile("catalogue/category/books"))]
# remove the first one because it corresponds to all the books
categories_urls = categories_urls[1:]
print(str(len(categories_urls)) + " fetched categories URLs")
print("Some examples:")
print(categories_urls[:5])

# to get all of the pages, we need to go through the 'next' buttons
# next button contains the pattern 'page'
# the previous button also contains this pattern!
# so, if there are two results, we take the second one that corresponds to next page

# 200 code means no error. 404 code means page was not found

# now try to iterate until we get a 404 code
pages_urls = []

new_page = "http://books.toscrape.com/catalogue/page-1.html"
while requests.get(new_page).status_code == 200:
    pages_urls.append(new_page)
    new_page = pages_urls[-1].split('-')[0] + "-" + str(int(pages_urls[-1].split("-")[1].split(".")[0]) + 1) + ".html"

print(str(len(pages_urls)) + " fetched page URLs")
print("Some examples:")
print(pages_urls[:5])

books_urls = []

for page in pages_urls:
    books_urls.extend(getBooksURLs(page))

print(str(len(books_urls)) + " fetched book URLs")
print("Some examples:")
print(books_urls[:5])

# get product data for everything
names = []
prices = []
nb_in_stock = []
img_urls = []
categories = []
ratings = []

for url in books_urls[:100]:
    # print(url)

    if requests.get(url).status_code != 404:
        soup = getAndParseURL(url)
        # print(soup)
        names.append(soup.find("div", class_ = re.compile("product_main")).h1.text)
        prices.append(soup.find("p", class_ = "price_color").text[2:]) # get rid of the pound sign
        nb_in_stock.append(re.sub("[^0-9]", "", soup.find("p", class_ = "instock availability").text))
        img_urls.append(url.replace("index.html","") + soup.find("img").get("src"))
        categories.append(soup.find("a",href = re.compile("../category/books/")).get("href").split("/")[3])
        ratings.append(soup.find("p", class_ = re.compile("star-rating")).get("class")[1])

print(names[:5])
print(prices[:5])
scraped_data = pd.DataFrame({"name": names, "price": prices, "in_stock": nb_in_stock, "image": img_urls,
                             "category": categories,
                             "rating": ratings})
print(scraped_data.head())

# for complex websites that render content in javascript, may want to use a browser automator like Selenium


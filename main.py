import requests
from bs4 import BeautifulSoup
import re

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
    soup = getAndParseURL(main_url)
    return(["/".join(url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in soup.findAll("article",
                                                                                            class_ = "product_pod")])

print(getBooksURLs(main_url)[0])

# find book categories URLs on the main page
# URL pattern is catalogue/category/books
soup = getAndParseURL(main_url)
categories_urls = [main_url + x.get('href') for x in soup.findAll("a", href=re.compile("catalogue/category/books"))]
print(categories_urls)
# remove the first one because it corresponds to all the books
categories_urls = categories_urls[1:]

print(str(len(categories_urls)) + " fetched categories URLs")
print("Some examples:")
print(categories_urls[:5])

# to get all of the pages, we need to go through the 'next' buttons
# next button contains the pattern 'page'
# the previous button also contains this pattern!
# so, if there are two results, we take the second one that corresponds to next page

# store all results in a list
pages_urls = [main_url]
soup = getAndParseURL(pages_urls[0])

while len(soup.findAll("a", href=re.compile("page"))) == 2 or len(pages_urls) == 1:
    new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.findAll("a", href=re.compile("page"))[-1].get("href")

    pages_urls.append(new_url)

    soup = getAndParseURL(new_url)

print(str(len(pages_urls)) + " fetched URLs")
print("Some examples:")
print(pages_urls[:5])
# we could have just created the list by incrementing page-X.html until 50
# increment the value until we get a 404 page

result = requests.get("http://books.toscrape.com/catalogue/page-50.html")
print("status code for page 50: " + str(result.status_code))

result = requests.get("http://books.toscrape.com/catalogue/page-51.html")
print("status code for page 51: " + str(result.status_code))

# 200 code means no error. 404 code means page was not found

# now try to iterate until we get a 404 code
pages_urls = []

new_page = "http://books.toscrape.com/catalogue/page-1.html"
while requests.get(new_page).status_code == 200:
    pages_urls.append(new_page)
    new_page = pages_urls[-1].split('-')[0] + "-" + str(int(pages_urls[-1].split("-")[1].split(".")[0]) + 1) + ".html"

print(str(len(pages_urls)) + " fetched URLs")
print("Some examples:")
print(pages_urls[:5])





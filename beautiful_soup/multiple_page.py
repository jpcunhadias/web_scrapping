import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

pager = soup.find('ul', class_='pager')
next_page = pager.find('li', class_='next').find('a')['href']

response = requests.get(url + next_page)
print(response.url)

# Output: https://books.toscrape.com/catalogue/page-2.html
# The output is the URL of the next page. This is how you can scrape multiple pages of a website.

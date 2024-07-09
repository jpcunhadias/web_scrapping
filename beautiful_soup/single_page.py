import pandas as pd
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, field_validator


class Book(BaseModel):
    title: str
    price: float

    @field_validator('price')
    def price_must_be_positive(cls, value):
        assert value > 0, 'price must be positive'

    def __repr__(self):
        return f'{self.title} - {self.price}'

    def __str__(self):
        return f'{self.title} - {self.price}'


url = 'https://books.toscrape.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

ordered_list_of_books = soup.find('ol', class_='row')
books = ordered_list_of_books.find_all('li')

df = pd.DataFrame(columns=['Title', 'Price'])

data = []

for book in books:
    title = book.find('h3').find('a')['title']
    price = book.find('p', class_='price_color').text

    data.append({'Title': title, 'Price': price})

df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
df['Price'] = df['Price'].str.extract(r'£(\d+\.\d+)').astype(float)

books = [Book(title=row['Title'], price=row['Price']) for index, row in df.iterrows()]

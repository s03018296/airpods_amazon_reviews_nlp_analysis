import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []
def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0",'Accept-Language': 'en-US, en;q=0.5'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
            'author': item.find('span', {'class': 'a-profile-name'}).text.strip(),
            'date': item.find('span', {'data-hook': 'review-date'}).text.strip(),
            'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
            'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
            'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            'helpful': item.find('span', {'data-hook': 'helpful-vote-statement'}).text.replace('people found this helpful', '').strip() if item.find('span', {'data-hook': 'helpful-vote-statement'}) else 0,
            'verified_purchase': 1 if item.find('span', {'data-hook': 'avp-badge'}) else 0,
            }
            data.append(review)
    except:
        pass

def get_pages_of_reviews(page_num):
    for x in range(1, page_num+1):
        try:
            soup = get_soup(f'https://www.amazon.ca/Gildan-Mens-T-Shirts-Assortment-Small/product-reviews/B077ZKF9ZN/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
            print(f'Getting page: {x}')
            get_reviews(soup)
            print(len(data))
        except:
            pass

if __name__ == '__main__':
    user_input = int(input("Enter pages of reviews: "))
    get_pages_of_reviews(user_input)
    df = pd.DataFrame(data)
    df.to_csv(r'tshirt_reviews.csv', index=False)

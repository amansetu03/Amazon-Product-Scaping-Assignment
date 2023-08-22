# https://www.amazon.in/s?k=bag&crid=TL4UOC9MP4N8&sprefix=bag%2Caps%2C308&ref=nb_sb_noss_1
# https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1
from bs4 import BeautifulSoup
import requests
import csv
import time


# function to extrect data from single page
def scrape_data_to_page(soup):
    product_details=[]
    # finding info about data
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    for product in products:
        url = product.find('a', {'class': 'a-link-normal s-no-outline'}).get('href')
        name = product.find('span',{'class':'a-size-medium a-color-base a-text-normal'}).text.strip()

        # Handle error when extracting price
        price_element = product.find('span',{'class':'a-price-whole'})
        price = price_element.text.strip() if price_element else None

        # rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split(' ')[0]
        # nor = product.find('span',{'class':'a-size-base s-underline-text'}) .text.strip().replace(',','') #Number of reviews
        
        # Handle error when extracting rating
        rating_element = product.find('span', {'class': 'a-icon-alt'})
        rating = rating_element.text.strip().split(' ')[0] if rating_element else None

        # Handle error when extracting Number of reviews
        nor_element = product.find('span', {'class':'a-size-base s-underline-text'})
        nor = nor_element.text.strip().replace(',', '') if nor_element else None
        p_url = f'https://www.amazon.in{url}'
        print(p_url)
        Acin = p_url.split('/')[-1]
        # d = get_pd()

        product_details.append({
            'URL': p_url,
            'Name':name,
            'Price':price,
            'Rating':rating,
            'Reviews':nor,
            'Acin':Acin,
        })
        # product_details.append({
        #     'URL': p_url,
        #     'Name':name,
        #     'Price':price,
        #     'Rating':rating,
        #     'Reviews':nor,
        #     'Acin':Acin,
        #     'Description':d
        # })

    return product_details

base_link = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1&page='
#save the info into file
filename = 'product_data.csv'
fields = ['URL', 'Name', 'Price', 'Rating', 'Reviews','Acin']
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()

    #Go for every page
    for page in range(1,21):
        count=0
        page_link=base_link+str(page)
        print(f"page no {page} Loading.......................")
        #requesting to page 
        while True:
            r = requests.get(page_link)
            if r.status_code == 200:
                html_text = r.text
                print(f"page no {page} Loaded")
                break
            if count==20:
                count=0
                print(f"page no {page} not responding")
                print("wait...")
                time.sleep(3)
            count+=1
        # after geting request parse the html
        soup = BeautifulSoup(html_text, 'html.parser')
        #calling function to get every product details
        pd=scrape_data_to_page(soup) 

        #write prodect info into csv file
        writer.writerows(pd)
        print(f"page {page} Data saved to", filename)


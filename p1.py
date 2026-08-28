from bs4 import BeautifulSoup
import pandas as pd
#import requests
import time
import random
from curl_cffi import requests

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "sec-ch-ua": (
        '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"'
    ),
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
}

#headers = {
#    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#    'Accept-Language': 'en-US,en;q=0.9',
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8'
#}
 
keywords = ["anker charger", "anker power bank", "anker cable", "anker hub"]
product_data = []
for keyword in keywords:
    formatted_keyword = keyword.replace(" ", "+") 
          


    for page in range(1, 20):
                url = f"https://www.amazon.com/s?k={formatted_keyword}&page={page}&crid=32KGEMTJZWBPO&qid=1787657320&sprefix=anke%2Caps%2C300&xpid=-1GYHvioGL4I5&ref=sr_pg_{page}"
                print(f"Scraping '{keyword}' - Page {page}...")
                html_text = requests.get(url, headers=headers,impersonate="chrome").text
       

                if "api-services-support@amazon.com" in html_text or "Type the characters you see in this image" in html_text:
                        print("Amazon blocked the request with a CAPTCHA!")
                        continue        
        
        
                soup = BeautifulSoup(html_text , 'lxml')
                products = soup.find_all('div', class_='puis-card-container puis-overflow-hidden s-card-container aok-relative desktop-list-view puis-include-content-margin puis puis-v31r26q2blk8vb2oed0mr6q94ft s-latency-cf-section puis-card-border')

                for product in products:  
                 
                        brand = product.find('span' , class_='a-size-medium a-color-base')
                        title = product.find('h2' , class_='a-size-medium a-spacing-none a-color-base a-text-normal')
                        prices = product.find('span',class_='a-offscreen')
                        rating_people = product.find('span',class_='a-size-mini puis-normal-weight-text s-underline-text')
                        rating = product.find('span',class_='a-size-small a-color-base')
                        img_tag = product.find('img', class_='s-image')
                        img_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else "no image"
                        link_tag =product.find('a',class_='a-link-normal s-line-clamp-2 puis-line-clamp-3-for-col-4-and-8 s-link-style a-text-normal')
                        href = link_tag['href'] if link_tag and link_tag.has_attr('href') else None
                        full_link = f"https://www.amazon.com{href}" if href else "no link"
                        product_data.append({"brand":brand.text if brand and brand else "no brand",
                                "title":title.span.text if title and title.span else "no product",
                                "price":prices.text if prices  else "no price",
                                "rating counts":rating_people.text if rating_people else "no rating_people",
                                "rating":rating.text if rating else "no rating",
                                "link": full_link,
                                "img": img_url})
                                
                
                
            
        
                time.sleep(random.randint(2, 4))
        
df = pd.DataFrame(product_data)
        
file_path = "amazon_products8.xlsx"
df.to_excel(file_path,index=False)     
        
print("succuss")
        
        #print(title.span.text if title and title.span else "no product")
        #print(prices.text if prices  else "no price")
        #print(rating_people.text if rating_people else "no rating_people")
        #print(rating.text if rating else "no rating")
    

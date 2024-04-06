import csv
import requests
import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup

def scrape_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'

    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []

    for product in soup.find_all('div', class_='sku-item'):
        name = product.find('h4', class_='sku-header').text.strip()

        price_element = product.find('div', class_='priceView-hero-price')
        if price_element:
            price = price_element.span.text.strip()
        else:
            price = 'N/A'

        rating_element = product.find('div', class_='rating')
        if rating_element:
            rating = rating_element.span.text.strip()
        else:
            rating = 'N/A'

        products.append({'Name': name, 'Price': price, 'Rating': rating})

    return products

def save_to_csv(data, filename):
    keys = data[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def scrape_and_save():
    url = url_entry.get()
    try:
        scraped_data = scrape_product_info(url)
        csv_filename = 'scraped_products.csv'
        save_to_csv(scraped_data, csv_filename)
        messagebox.showinfo('Success', f'Scraped data saved to {csv_filename}')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {str(e)}')


root = tk.Tk()
root.title('E-commerce Web Scraper')


url_label = tk.Label(root, text='Enter the Best Buy URL:')
url_label.pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)
scrape_button = tk.Button(root, text='Scrape and Save', command=scrape_and_save)
scrape_button.pack(pady=10)


root.mainloop()

"""
DISCLAIMER:
This script is intended for educational purposes only. The use of this script for scraping Amazon's website may violate Amazon's Terms of Service.

Amazon's Terms of Service prohibit unauthorized access to their website using automated methods, including scraping. By using this script, you acknowledge that scraping Amazon's website may result in your IP address being blocked and could lead to legal action.

**Use Responsibly**:
- The script is provided for learning and personal use only. Any commercial or large-scale use is strictly prohibited.
- You should **always respect robots.txt** and other site-specific rules.
- Avoid overloading Amazon's servers by including sufficient delays between requests.
- For legitimate use of Amazon product data, consider using Amazon's official **Product Advertising API** or other authorized methods.

Please read and understand Amazon's Terms of Service and robots.txt file before using this script. The author of this script is not responsible for any consequences arising from the use of this code.
"""

__author__ = 'Anmol Gawande'

import requests
from datetime import datetime
import time
import csv
import random
from bs4 import BeautifulSoup


# Function to scrape data from the product page
def scrape_product_data(url, index):
    # Send a GET request to the URL
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"Getting response from index - {index}...!!!")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract relevant data
        product_name = soup.select('span#productTitle')[0].text.strip() if soup.select('span#productTitle') else 'n/a'
        price = soup.select('span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay span.a-price-whole')[0].text.strip() if soup.select('span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay span.a-price-whole') else 'n/a'
        image = soup.select('div#imgTagWrapperId img')[0].get('src') if soup.select('div#imgTagWrapperId img') else 'n/a'
        rating = soup.select('span#acrPopover span.a-size-base.a-color-base')[0].text.strip() if soup.select('span#acrPopover span.a-size-base.a-color-base') else 'n/a'
        reviews = soup.select('span#acrCustomerReviewText')[0].text.replace(',', '').replace('ratings', '').replace('rating', '').strip() if soup.select('span#acrCustomerReviewText') else 'n/a'
        stock = soup.select('div#addToCart_feature_div span.a-button-text')[0].text.strip() if soup.select('div#addToCart_feature_div span.a-button-text') else 'n/a'
        if 'add' in stock.lower():
            stock = 'In Stock'
        else:
            stock = 'Out of Stock'

        # Return data as a dictionary
        return {
            'product_name': product_name,
            'price': price,
            'image': image,
            'rating': rating,
            'reviews': reviews,
            'stock_status': stock
        }
    else:
        return None  # Return None if request fails


# Generate a unique filename for the output file based on current date and time
def generate_unique_output_filename():
    current_datetime = datetime.now()
    filename = current_datetime.strftime('output_%Y%m%d_%H%M%S.tsv')
    return filename


# Read the input file, scrape data, and write it to a new output file
def process_and_update_output(input_file):
    # Generate a unique output filename
    output_file = generate_unique_output_filename()

    # Open the input file to read the URLs
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        tsv_reader = csv.reader(infile, delimiter='\t')
        # Skip the header row if present
        next(tsv_reader, None)

        # Open the new output file in write mode
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            tsv_writer = csv.writer(outfile, delimiter='\t')

            # Write the header row to the output file
            tsv_writer.writerow(['Index', 'Name', 'Price', 'Image', 'Rating', 'Reviews', 'Stock', 'Date', 'Time', 'Unique ID'])

            # Iterate through each row in the input file
            for row in tsv_reader:
                index, url, region, unique_identifier = row

                # Scrape the product data
                product_data = scrape_product_data(url, index)

                if product_data:
                    # Get current date and time
                    current_datetime = datetime.now()
                    current_date = current_datetime.strftime('%Y-%m-%d')
                    current_time = current_datetime.strftime('%H:%M:%S')

                    # Prepare row with data, date and time
                    output_row = [
                        index,
                        product_data['product_name'],
                        product_data['price'],
                        product_data['image'],
                        product_data['rating'],
                        product_data['reviews'],
                        product_data['stock_status'],
                        current_date,
                        current_time,
                        unique_identifier,
                    ]
                    # Write the row to the output file
                    tsv_writer.writerow(output_row)

                # Optional: Add a delay to prevent overloading the server or getting blocked
                delay = random.randint(5, 10)
                print(f"Waiting for {delay} seconds...")
                time.sleep(delay)

    print(f"Data has been saved to {output_file}")


# Main - uncomment the below code to run on local machine

# if __name__ == "__main__":
#     # Specify input file path
#     input_file = 'input_urls.tsv'
#
#     # Call the function to process and update the output file
#     process_and_update_output(input_file)

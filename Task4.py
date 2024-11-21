import requests
from bs4 import BeautifulSoup
import csv
import random

# Function to fetch the webpage content with rotating User-Agents and headers
def fetch_webpage(url):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    ]
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve webpage: {response.status_code}")
        return None

# Function to parse the HTML and extract product (book) information
def parse_html_and_extract_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all books in the HTML (class "product_pod" contains the book details)
    books = soup.find_all('article', class_='product_pod')
    extracted_data = []

    for book in books:
        # Get the book title
        title = book.h3.a['title']

        # Get the book price
        price = book.find('p', class_='price_color').get_text(strip=True)

        # Get the book rating (if available)
        rating_class = book.find('p', class_='star-rating')['class']
        rating = rating_class[1] if rating_class else 'No rating'

        # Store book information as a dictionary
        extracted_data.append({
            'Book Title': title,
            'Price': price,
            'Rating': rating
        })
    
    return extracted_data

# Function to save the extracted data into a CSV file
def save_to_csv(data, filename='books.csv'):
    # Define the CSV file headers
    fieldnames = ['Book Title', 'Price', 'Rating']

    # Write data to CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data saved to {filename}")

# Main function to scrape the website and save the data
def main():
    url = "http://books.toscrape.com/"  # Books to Scrape URL

    # Step 1: Fetch the webpage content
    html_content = fetch_webpage(url)
    if html_content is None:
        return

    # Step 2: Parse the HTML and extract product (book) information
    book_data = parse_html_and_extract_data(html_content)

    # Step 3: Save the extracted data into a CSV file
    if book_data:
        save_to_csv(book_data)
    else:
        print("No book data found")

if __name__ == "__main__":
    main()
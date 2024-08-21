import requests
from bs4 import BeautifulSoup
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraping.log"),
        logging.StreamHandler()
    ]
)

# Base URL
base_url = "https://www.publico.pt/autor/jorge-mourinha?page="

# Function to scrape a single page
def scrape_page(page_num):
    url = base_url + str(page_num)
    response = requests.get(url)
    page_results = []

    # Check if the request was successful
    if response.status_code == 200:
        logging.info(f"Scraping page {page_num}...")

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all div elements with the class 'media-object-section'
        media_sections = soup.find_all('div', class_='media-object-section')

        for section in media_sections:
            # Initialize an empty dictionary for storing the extracted data
            data = {}

            # Extract the href attribute
            link = section.find('a')
            if link and 'href' in link.attrs:
                data['href'] = link['href']

            # Extract the ratingValue if available
            rating_meta = section.find('meta', itemprop='ratingValue')
            if rating_meta:
                data['ratingValue'] = rating_meta['content']

            # Extract the headline
            headline = section.find('h4', class_='headline')
            if headline:
                data['headline'] = headline.text.strip()

            # Extract the review genre and name
            review_heading = section.find('h5', class_='review__heading')
            if review_heading:
                genre = review_heading.find('span', class_='review__genre')
                name = review_heading.find('span', class_='review__name')

                if genre:
                    data['review_genre'] = genre.text.strip()
                if name:
                    data['review_name'] = name.text.strip()

            # Extract the datetime
            time_tag = section.find('time', class_='dateline')
            if time_tag and 'datetime' in time_tag.attrs:
                data['datetime'] = time_tag['datetime']

            # Only add the data to the results if it contains the necessary fields
            if 'href' in data and 'ratingValue' in data and 'headline' in data:
                page_results.append(data)
    else:
        logging.warning(f"Failed to retrieve page {page_num}. Status code: {response.status_code}")

    return page_results

# List to store results from all pages
all_results = []

# Use ThreadPoolExecutor to parallelize the scraping process
with ThreadPoolExecutor(max_workers=10) as executor:
    # Create a list of future tasks
    future_to_page = {executor.submit(scrape_page, page_num): page_num for page_num in range(1, 555)}

    # Process the results as they complete
    for future in as_completed(future_to_page):
        page_num = future_to_page[future]
        try:
            page_results = future.result()
            all_results.extend(page_results)
            logging.info(f"Completed scraping of page {page_num} with {len(page_results)} results.")
        except Exception as e:
            logging.error(f"Page {page_num} generated an exception: {e}")

# Convert the results to a JSON object
all_results_json = json.dumps(all_results, ensure_ascii=False, indent=4)

# Save the JSON to a file
with open("results.json", "w", encoding="utf-8") as file:
    file.write(all_results_json)

# Print completion message
logging.info("Scraping completed and saved to results.json")

import json
import csv
from datetime import datetime
from collections import defaultdict

# Increase the field size limit to a large value
csv.field_size_limit(10**8)

# Load the JSON file
with open('../scrape/results.json', 'r', encoding='utf-8') as json_file:
    reviews = json.load(json_file)

# Initialize a defaultdict to store imdb_ids by review_name
imdb_dict = defaultdict(list)

# Open and read the TSV file using DictReader for more efficiency
with open('title.akas.tsv', 'r', encoding='utf-8') as tsv_file:
    reader = csv.DictReader(tsv_file, delimiter='\t')

    # Iterate over rows in the TSV file
    for row in reader:
        if row['region'] == 'PT':  # Assuming you have a header and 'PT' is the correct key
            imdb_id = row['titleId']  # Replace with the actual header name for the IMDb ID
            title = row['title']
            imdb_dict[title].append(imdb_id)

# Update the JSON objects with matching IMDb IDs
for review in reviews:
    name = review.get('review_name')
    if name in imdb_dict:
        review['imdb'] = imdb_dict[name]

# Sort the JSON objects by the datetime field
reviews_sorted = sorted(reviews, key=lambda x: datetime.strptime(x['datetime'], '%a, %d %b %Y %H:%M:%S %Z'))

# Save the updated and sorted JSON to a new file
with open('updated_reviews_sorted.json', 'w', encoding='utf-8') as outfile:
    json.dump(reviews_sorted, outfile, ensure_ascii=False, indent=4)

print("Updated and sorted JSON file has been saved as 'updated_reviews_sorted.json'")

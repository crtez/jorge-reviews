import json
import csv
from datetime import datetime

# Load IMDb data from TSV file
imdb_data = {}
with open("../imdb_data/title.basics.tsv", encoding='utf-8') as tsvfile:
    reader = csv.DictReader(tsvfile, delimiter='\t')
    for row in reader:
        imdb_data[row['tconst']] = row['startYear']

# Function to find the closest year
def find_closest_imdb(imdb_ids, review_date):
    closest_id = None
    closest_year = None
    review_year = datetime.strptime(review_date, "%a, %d %b %Y %H:%M:%S %Z").year

    for imdb_id in imdb_ids:
        if imdb_id in imdb_data:
            imdb_year = imdb_data[imdb_id]
            if imdb_year != '\\N':  # Ignore entries without a valid year
                imdb_year = int(imdb_year)
                if imdb_year <= review_year:
                    if closest_year is None or (review_year - imdb_year) < (review_year - closest_year):
                        closest_year = imdb_year
                        closest_id = imdb_id

    return closest_id

# Load JSON data
with open("final.json", "r", encoding='utf-8') as infile:
    data = json.load(infile)

# Process entries
for entry in data:
    if 'imdb' in entry and len(entry['imdb']) > 1:
        closest_imdb = find_closest_imdb(entry['imdb'], entry['datetime'])
        if closest_imdb:
            entry['imdb'] = [closest_imdb]
            print(f"Updated entry for '{entry['review_name']}': {closest_imdb}")
        else:
            print(f"No valid IMDb entry found for '{entry['review_name']}'")

# Save to new JSON file
with open("../viz/final_for_real.json", "w", encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False, indent=4)

print("Processing complete. Results saved to 'final_for_real.json'.")

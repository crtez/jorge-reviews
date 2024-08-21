import json
import requests

# Load your JSON file
with open('updated_reviews_sorted_2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Find entries with an empty 'imdb' field
missing_imdb_entries = [entry for entry in data if 'imdb' in entry and not entry['imdb']]
print(f"Found {len(missing_imdb_entries)} entries with an empty IMDb field.")

# Function to fetch IMDb ID
def fetch_imdb_id(review_name):
    try:
        print(f"Fetching IMDb ID for '{review_name}'...")
        response = requests.get(f'https://v3.sg.media-imdb.com/suggestion/x/{review_name}.json')
        response_data = response.json()
        if 'd' in response_data and len(response_data['d']) > 0:
            imdb_id = response_data['d'][0]['id']
            print(f"Found IMDb ID '{imdb_id}' for '{review_name}'.")
            return imdb_id
        else:
            print(f"No IMDb ID found for '{review_name}'.")
    except Exception as e:
        print(f"Error fetching IMDb ID for '{review_name}': {e}")
    return None

# Update entries with the fetched IMDb ID
for i, entry in enumerate(missing_imdb_entries, start=1):
    review_name = entry.get('review_name', '').strip()
    if review_name:  # Skip if review_name is an empty string
        imdb_id = fetch_imdb_id(review_name)
        if imdb_id:
            entry['imdb'] = [imdb_id]
    else:
        print(f"Skipping entry {i} with empty review_name.")
    print(f"Processed {i}/{len(missing_imdb_entries)} entries.")

# Save the updated data as a new JSON file
with open('final.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Updated entries saved to 'final.json'.")

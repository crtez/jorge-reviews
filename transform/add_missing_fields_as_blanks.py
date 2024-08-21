import json

# Define the file paths
input_file = 'updated_reviews_sorted.json'  # Replace with your input file name
output_file = 'updated_reviews_sorted_2.json'  # Replace with your desired output file name

# Keys that should be present in every JSON entry
required_keys = ["href", "ratingValue", "headline", "review_genre", "review_name", "datetime", "imdb"]

# Read the JSON file
with open(input_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Go through each entry and add missing keys with blank values
for entry in json_data:
    for key in required_keys:
        if key not in entry:
            # Assign a blank value based on the expected data type
            if key == "imdb":
                entry[key] = []
            else:
                entry[key] = ""

# Write the updated JSON data back to a file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=4, ensure_ascii=False)

print(f"Updated JSON data written to {output_file}")

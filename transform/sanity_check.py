import json

# Load JSON files
with open('../viz/final_for_real.json', 'r', encoding="utf-8") as f1, open('../scrape/results.json', 'r',encoding="utf-8") as f2:
    list1 = json.load(f1)
    list2 = json.load(f2)

# Extract the href values from each list of JSON entries
hrefs1 = {entry['href'] for entry in list1 if 'href' in entry}
hrefs2 = {entry['href'] for entry in list2 if 'href' in entry}

# Compare the sets of hrefs
if hrefs1 == hrefs2:
    print("The sets of hrefs in both JSON files are the same.")
else:
    print("The sets of hrefs in the JSON files are different.")
    print("Hrefs only in file1:", hrefs1 - hrefs2)
    print("Hrefs only in file2:", hrefs2 - hrefs1)

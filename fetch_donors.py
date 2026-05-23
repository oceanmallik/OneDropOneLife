import csv
import json
import urllib.request

# Your exact published Google Sheets CSV URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQZkS9QtZeWOZUtbWkQN3Z7kbtv0itx6m7xnqwx-EpYkq0FHvpZOYohijb3uS8VVst7sOOKpRAJWcBs/pub?gid=0&single=true&output=csv"
OUTPUT_FILE = "donors.json"

# HEADER MAPPING CONFIGURATION
HEADER_MAP = {
    "Name": ["Name", "Full Name", "Donor Name"],
    "ID": ["ID", "Student ID", "Varsity ID"],
    "Blood Group": ["Blood Group", "Blood Type", "Blood"],
    "Address": ["Address", "Location", "Area", "Present Address"],
    "Contact Number": ["Contact Number", "Phone Number", "Phone", "Contact", "Mobile"]
}

# SETTINGS FOR IGNORING RAW ROWS
# If row 1 is a merged title banner, set this to 1. If rows 1 and 2 are title/notes, set to 2.
ROWS_TO_SKIP_AT_TOP = 1

def normalize_row(raw_row):
    normalized = {}
    
    for expected_key, alternative_names in HEADER_MAP.items():
        found = False
        for alt_name in alternative_names:
            if alt_name in raw_row:
                normalized[expected_key] = raw_row[alt_name].strip()
                found = True
                break
        if not found:
            normalized[expected_key] = ""
            
    return normalized

def fetch_data():
    try:
        print("Fetching latest CSV data from Google Sheets...")
        response = urllib.request.urlopen(SHEET_URL)
        raw_lines = [line.decode('utf-8') for line in response.readlines()]
        
        # --- FEATURE 1: Skip top title rows ---
        if ROWS_TO_SKIP_AT_TOP > 0:
            print(f"Skipping the first {ROWS_TO_SKIP_AT_TOP} line(s) of the sheet...")
            # Slice the list to remove the top decorative rows
            data_lines = raw_lines[ROWS_TO_SKIP_AT_TOP:]
        else:
            data_lines = raw_lines

        reader = csv.DictReader(data_lines)
        
        donor_list = []
        for row in reader:
            clean_row = normalize_row(row)
            
            # --- FEATURE 2: Ignore invalid, blank, or broken rows ---
            # If a row doesn't have a Name and doesn't have an ID, it's an accidental row. Ignore it.
            if not clean_row["Name"] and not clean_row["ID"]:
                print("Skipped an empty or non-donor row.")
                continue
                
            donor_list.append(clean_row)
        
        # Save as a formatted JSON database file in the root
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(donor_list, f, indent=4, ensure_ascii=False)
            
        print(f"Success! {len(donor_list)} donor profiles normalized and saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error fetching data from Google Sheets: {e}")

if __name__ == "__main__":
    fetch_data()
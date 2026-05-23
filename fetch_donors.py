import csv
import json
import urllib.request
import re

# Your exact published Google Sheets CSV URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQZkS9QtZeWOZUtbWkQN3Z7kbtv0itx6m7xnqwx-EpYkq0FHvpZOYohijb3uS8VVst7sOOKpRAJWcBs/pub?gid=0&single=true&output=csv"
OUTPUT_FILE = "donors.json"

# HEADER MAPPING CONFIGURATION
HEADER_MAP = {
    "Name": ["Name", "Full Name", "Donor Name"],
    "ID": ["ID", "Student ID", "Varsity ID"],
    "Blood Group": ["Blood Group", "Blood Type", "Blood", "Group"],
    "Address": ["Address", "Location", "Area", "Present Address"],
    "Contact Number": ["Contact Number", "Phone Number", "Phone", "Contact", "Mobile"]
}

ROWS_TO_SKIP_AT_TOP = 1

def clean_bangladeshi_phone(raw_phone):
    """
    Cleans and normalizes alternative input formats into a standardized 13-digit 
    string starting explicitly with '8801XXXXXXXX'.
    """
    if not raw_phone:
        return ""
        
    # Step 1: Keep only numbers (removes +, -, spaces, or brackets)
    digits = re.sub(r'\D', '', str(raw_phone))
    
    if not digits:
        return ""

    # Step 2: Handle 11-digit entry format (e.g., 017XXXXXXXX)
    if len(digits) == 11 and digits.startswith("01"):
        return f"88{digits}"
        
    # Step 3: Handle 10-digit entry format (e.g., 17XXXXXXXX if leading zero dropped)
    if len(digits) == 10 and digits.startswith("1"):
        return f"880{digits}"
        
    # Step 4: Handle 13-digit format (e.g., 8801XXXXXXXX)
    if len(digits) == 13 and digits.startswith("8801"):
        return digits

    # Fallback: If it's a completely weird length or landline number, return digits as-is
    return digits

def normalize_row(raw_row):
    """
    Translates a row from whatever headers the Google Sheet uses
    into the exact keys the website's frontend expects.
    """
    normalized = {}
    
    for expected_key, alternative_names in HEADER_MAP.items():
        found = False
        for alt_name in alternative_names:
            if alt_name in raw_row:
                val = raw_row[alt_name].strip()
                
                # If processing the Contact Number, pass it through our normalization engine
                if expected_key == "Contact Number":
                    val = clean_bangladeshi_phone(val)
                    
                normalized[expected_key] = val
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
        
        if ROWS_TO_SKIP_AT_TOP > 0:
            print(f"Skipping the first {ROWS_TO_SKIP_AT_TOP} line(s) of the sheet...")
            data_lines = raw_lines[ROWS_TO_SKIP_AT_TOP:]
        else:
            data_lines = raw_lines

        reader = csv.DictReader(data_lines)
        
        donor_list = []
        for row in reader:
            clean_row = normalize_row(row)
            
            if not clean_row["Name"] and not clean_row["ID"]:
                continue
                
            donor_list.append(clean_row)
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(donor_list, f, indent=4, ensure_ascii=False)
            
        print(f"Success! {len(donor_list)} donor profiles normalized and saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error fetching data from Google Sheets: {e}")

if __name__ == "__main__":
    fetch_data()
# 🩸 OneDropOneLife — BloodInfo

> *"5 Amenities Keep You Alive. The 6th Saves You When It Matters Most."*

**BloodInfo** is a blood donor discovery platform built for the Daffodil International University community. It connects people in urgent need of blood with registered donors — quickly, cleanly, and without friction.

🌐 **Live Site:** [blood.oceanmallik.com](https://blood.oceanmallik.com)

---

## ✨ Features

- **Donor Search & Filter** — Filter registered donors by blood group (A+, A−, B+, B−, O+, O−, AB+, AB−)
- **Location Sorting** — Sort or filter donors by dormitory/location (YKSG 1–3, RASG 1–2, A–Z)
- **Dynamic Donor Cards** — Donor profiles are rendered client-side from a live JSON feed
- **Google Sheets Integration** — Donor data syncs automatically from a published Google Sheet via a Python script
- **Bangladeshi Phone Normalization** — Contact numbers are cleaned and standardized to the `8801XXXXXXXXX` format
- **Dark-themed UI** — A minimal, urgent-first design built with plain HTML, CSS, and vanilla JavaScript
- **GitHub Actions CI/CD** — Automated deployment pipeline via `.github/workflows`

---

## 🗂️ Project Structure

```
OneDropOneLife/
├── index.html          # Main landing page and donor search UI
├── style.css           # Dark-themed stylesheet
├── app.js              # Client-side donor rendering and filter/sort logic
├── donors.json         # Auto-generated donor data (do not edit manually)
├── fetch_donors.py     # Python script to sync donors from Google Sheets
├── favicon.png         # Site favicon
├── CNAME               # Custom domain config for GitHub Pages
└── .github/
    └── workflows/      # GitHub Actions for automated deployment
```

---

## 🚀 Getting Started

### Prerequisites

- A modern web browser (for the site itself)
- Python 3.x (for the data sync script)

### Run Locally

Clone the repository and open `index.html` directly in your browser — no build step required.

```bash
git clone https://github.com/oceanmallik/OneDropOneLife.git
cd OneDropOneLife
# Open index.html in your browser
```

### Sync Donor Data from Google Sheets

The `donors.json` file is generated from a published Google Sheet. To refresh it:

```bash
python fetch_donors.py
```

This fetches the latest CSV from the configured sheet URL, normalizes the data (including phone numbers), and overwrites `donors.json`.

> **Note:** The Google Sheets URL is hardcoded in `fetch_donors.py`. Update the `SHEET_URL` variable if the source sheet changes.

---

## 📋 Donor Data Format

Each entry in `donors.json` follows this structure:

```json
{
  "Name": "Ocean Mallik",
  "ID": "253-35-087",
  "Blood Group": "O+",
  "Address": "YKSG-3",
  "Contact Number": "8801326174513"
}
```

The `fetch_donors.py` script accepts flexible column headers from the Google Sheet (e.g., `"Phone Number"`, `"Mobile"`, `"Present Address"`) and maps them to these standardized keys automatically.

---

## 🔧 Configuration

To point the data pipeline at a different Google Sheet, update the `SHEET_URL` in `fetch_donors.py`:

```python
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/YOUR_SHEET_ID/pub?gid=0&single=true&output=csv"
```

To skip header rows in the sheet, adjust:

```python
ROWS_TO_SKIP_AT_TOP = 1
```

---

## 🤝 Become a Donor

Want to register as a donor? Visit the [Daffodil International University Blood Donation Club](https://clubs.daffodilvarsity.edu.bd/club/bdc).

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Data | JSON, Google Sheets (CSV export) |
| Backend script | Python 3 (stdlib only) |
| Hosting | GitHub Pages |
| CI/CD | GitHub Actions |

---

## 📄 License

This project is open source. Contributions and forks are welcome.

---

*Made with ❤️ to save lives, one drop at a time.*

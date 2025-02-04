import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin  # Import urljoin to handle URLs correctly

# Correct base URL
BASE_URL = "https://www.fueleconomy.gov"
URL = "https://www.fueleconomy.gov/feg/download.shtml"

# Create directory for downloads
SAVE_DIR = "../fuel_economy_data/"
os.makedirs(SAVE_DIR, exist_ok=True)

# Fetch the webpage
try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"❌ Failed to fetch website: {e}")
    exit()

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Extract ZIP file links
zip_links = []
for link in soup.find_all("a", href=True):
    if link["href"].endswith(".zip"):
        zip_url = urljoin(URL, link["href"])  # ✅ Fixes incorrect URL joining
        zip_links.append(zip_url)
        print(f"🔗 Found ZIP: {zip_url}")  # Debugging output

# Check if any ZIP links were found
if not zip_links:
    print("❌ No ZIP files found on the page!")
    exit()

# Download ZIP files
for zip_url in zip_links:
    zip_name = zip_url.split("/")[-1]  
    zip_path = os.path.join(SAVE_DIR, zip_name)

    try:
        print(f"⬇️ Downloading {zip_name}...")
        zip_response = requests.get(zip_url, stream=True, timeout=20)
        zip_response.raise_for_status()  

        with open(zip_path, "wb") as file:
            for chunk in zip_response.iter_content(chunk_size=1024):
                file.write(chunk)

        print(f"✅ Saved: {zip_path}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download {zip_name}: {e}")

print("🎉 All ZIP files downloaded successfully!")

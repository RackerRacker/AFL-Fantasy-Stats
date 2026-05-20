import requests
from bs4 import BeautifulSoup
import csv
import time  # Imported to add delays between page requests

# 1. The Base URL with a placeholder '{}' for the page number.
# YOU MUST UPDATE THIS based on what the URL looks like when you click page 2 on the website.
base_url = "https://finalsiren.com/AFLPlayerStats.asp?SeasonID=2023&Page={}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# This master list will hold data from ALL pages
all_table_data = []
extract_headers = True  # Flag to ensure we only get the table headers once

# 2. Set the range of pages you want to scrape (e.g., pages 1 through 5)
# range(1, 6) means it will do 1, 2, 3, 4, 5. 
for page_num in range(1, 15):
    
    # Insert the current page number into the URL
    current_url = base_url.format(page_num)
    print(f"Scraping Page {page_num}: {current_url}")
    
    response = requests.get(current_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table') 
        
        if table:
            rows = table.find_all('tr')
            
            for index, row in enumerate(rows):
                cells = row.find_all(['th', 'td'])
                row_data = [cell.text.strip() for cell in cells]
                
                if row_data:
                    # If this is the header row (<th>)
                    if row.find('th'):
                        # Only add the header row from the very first page
                        if extract_headers and page_num == 1:
                            all_table_data.append(row_data)
                            extract_headers = False
                    # If it's a normal data row (<td>)
                    else:
                        all_table_data.append(row_data)
        else:
            print(f"  -> No table found on page {page_num}. Ending loop.")
            break # Stop the loop if we hit a page with no data
            
    else:
        print(f"  -> Failed to fetch page {page_num}. Status Code: {response.status_code}")
        break # Stop the loop if the server throws an error
        
    # 3. BE POLITE: Pause for 2 seconds before requesting the next page
    time.sleep(2)

print(f"\nFinished scraping. Collected {len(all_table_data)} total rows across all pages.")

# 4. Save everything to a single CSV file
filename = 'afl_player_stats_2023.csv'

with open(filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(all_table_data)

print(f"Data successfully saved to {filename}")
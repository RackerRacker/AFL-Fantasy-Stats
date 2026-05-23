import requests
from bs4 import BeautifulSoup
import csv
import time
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


season = "2021"
folder_name = f"Player-Stats-{season}-Rounds"
base_url = f"https://finalsiren.com/AFLPlayerStats.asp?SeasonID={season}&Round={{}}&Page={{}}"

# 2. Define the rounds you want to scrape. 
# Update this list based on the exact URL parameters the website uses for rounds.
# For example: "0-1" (Opening Round?), "1", "2", "3", etc.
rounds_to_scrape = ["1-1", "2-1", "3-1", "4-1", "5-1", "6-1", "7-1", "8-1", "9-1", "10-1", "11-1", "12-1", "13-1", "14-1", "15-1", "16-1", "17-1", "18-1", "19-1", "20-1", "21-1", "22-1", "23-1", "1-2", "2-2", "3-2", "4-2"] 

def get_total_pages(season, round_id):
    """Dynamically finds the total number of pages for a specific season and round."""
    url = f"https://finalsiren.com/AFLPlayerStats.asp?SeasonID={season}&Round={round_id}&Page=1"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return 0
        
    soup = BeautifulSoup(response.text, 'html.parser')
    pagination_ul = soup.find('ul', class_='pagination')
    
    if not pagination_ul:
        return 1
        
    page_numbers = []
    for link in pagination_ul.find_all(['a', 'span']):
        text = link.text.strip()
        if text.isdigit():
            page_numbers.append(int(text))
            
    return max(page_numbers) if page_numbers else 1

# --- MAIN ROUND LOOP ---
for round_id in rounds_to_scrape:
    print(f"\n--- Season {season} | Round {round_id} ---")
    
    round_data = []
    extract_headers = True 
    
    total_pages = get_total_pages(season, round_id)
    
    if total_pages == 0:
        print("Skipping due to connection error.")
        continue

    # --- PAGE LOOP ---
    for page_num in range(1, total_pages + 1):
        
        url = f"https://finalsiren.com/AFLPlayerStats.asp?SeasonID={season}&Round={round_id}&Page={page_num}"
        print(f"  Scraping Page {page_num}/{total_pages}...")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            
            if table:
                rows = table.find_all('tr')
                
                # If the table only has a header but no players, break the page loop early
                if len(rows) <= 1:
                    break
                
                for row in rows:
                    cells = row.find_all(['th', 'td'])
                    row_data_list = [cell.text.strip() for cell in cells]
                    
                    if row_data_list:
                        if row.find('th'):
                            if extract_headers:
                                round_data.append(row_data_list)
                                extract_headers = False
                        else:
                            round_data.append(row_data_list)
            else:
                print(f"    -> No table found on page {page_num}.")
        else:
            print(f"    -> Server returned error {response.status_code}.")
            
        time.sleep(2) # Polite delay

    # --- SAVE FILE INTO THE FOLDER ---
    if len(round_data) > 1: 
        # Safely combine the folder name and the CSV file name
        file_path = os.path.join(folder_name, f'afl_stats_round_{rounds_to_scrape.index(round_id) + 1}.csv')
        
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(round_data)
            
        print(f"SUCCESS: Saved {len(round_data)-1} players to {file_path}")
    else:
        print(f"Skipped saving: No data for Season {season}, Round {round_id}.")

print("\nFinished! Check the folder for your files.")
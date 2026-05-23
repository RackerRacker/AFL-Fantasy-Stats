import requests
from bs4 import BeautifulSoup
import csv

# The specific URL you provided
url = "https://www.footywire.com/afl/footy/dream_team_round?year=2025&round=1&p=&s=T"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"Fetching data from Footywire...\n{url}\n")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. Target the exact table using the ID from your screenshot
    table = soup.find('table', id='supercoach-content-table')
    
    if table:
        table_data = []
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['th', 'td'])
            
            # Clean up the text, removing extra spaces and newlines
            row_data = [cell.text.strip() for cell in cells]
            
            # 2. Filter out empty rows
            # Footywire sometimes uses spacer rows that are just empty <td> tags.
            # `any(row_data)` ensures we only keep rows that actually have text in them.
            if any(row_data):
                table_data.append(row_data)
        
        # 3. Save the data to a CSV file
        filename = 'footywire_dream_team_2025_r1.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(table_data)
            
        print(f"SUCCESS: Saved {len(table_data)} rows to {filename}")
        
        # Print a quick preview of the top 3 rows
        print("\n--- Data Preview ---")
        for row in table_data[:3]:
            print(row)
            
    else:
        print("Could not find the table with id='supercoach-content-table'.")
else:
    print(f"Failed to fetch the page. Status Code: {response.status_code}")
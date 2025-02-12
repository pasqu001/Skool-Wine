import requests
import csv

# API Endpoint
url = "https://www.burrowingowlwine.ca/wp-admin/admin-ajax.php"

# Wines and Available Years
wine_products = [
    {"Product Name": "Athene", "Years": [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]},
    {"Product Name": "Cabernet Franc", "Years": [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]},
    {"Product Name": "Cabernet Sauvignon", "Years": [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]},
    {"Product Name": "Chardonnay", "Years": [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]},
    {"Product Name": "Coruja", "Years": ["NV"]},
    {"Product Name": "Malbec", "Years": [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]},
    {"Product Name": "Meritage", "Years": [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]},
    {"Product Name": "Merlot", "Years": [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]},
    {"Product Name": "Pinot Gris", "Years": [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]},
    {"Product Name": "Pinot Noir", "Years": [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]},
    {"Product Name": "Rosé", "Years": [2021, 2022, 2023]},
    {"Product Name": "Sauvignon Blanc", "Years": [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]},
    {"Product Name": "Syrah", "Years": [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]},
    {"Product Name": "Tempranillo", "Years": [2013]},
    {"Product Name": "Viognier", "Years": [2017, 2018, 2019, 2020, 2021, 2022]}
]

# Request
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://www.burrowingowlwine.ca",
    "Referer": "https://www.burrowingowlwine.ca/wine/"
}

# Output File
csv_filename = "wine_data.csv"

# Open Output File
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Wine", "Year", "URL"])
    
    # Loop Through Wines and Years
    for wine in wine_products:
        product_name = wine["Product Name"]
        for year in wine["Years"]:
            payload = {
                "action": "filter_wines",
                "title": product_name,
                "vintage": str(year)
            }
            
            response = requests.post(url, data=payload, headers=headers)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("success") and data.get("data"):
                        wine_data = data["data"][0]
                        files_data = wine_data.get("files", {})
                        
                        if "_meta_files_pdf" in files_data and "url" in files_data["_meta_files_pdf"]:
                            featured_sheet_url = files_data["_meta_files_pdf"]["url"]
                            print(f"{product_name} ({year}): {featured_sheet_url}")
                            writer.writerow([product_name, year, featured_sheet_url])
                        else:
                            print(f"Skipping {product_name} ({year}): No PDF URL available")
                except ValueError:
                    print(f"Failed to parse JSON for {product_name} ({year})")
            else:
                print(f"Request failed for {product_name} ({year}) with status {response.status_code}")

print(f"CSV file '{csv_filename}' has been created successfully.")


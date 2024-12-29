import csv
import json

csv_file_path = "news_data.csv"

def get_unique_companies(csv_file):
    try:
        unique_companies = {}
        with open(csv_file, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                company_code = row['Company_code']
                company_name = row['Company_whole_name']
                if company_code not in unique_companies:
                    unique_companies[company_code] = company_name
        return(json.dumps(unique_companies, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return {}
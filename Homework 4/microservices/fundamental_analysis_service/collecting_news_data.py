import os
import requests
import html
import re
import pdfplumber
from io import BytesIO
from html.parser import HTMLParser
import csv
from multiprocessing import Pool
from datetime import datetime


CSV_FILE_PATH = "news_data.csv"

parser = HTMLParser()


def process_news(data):
    try:
        document_id = data.get('documentId', '')
        content = data.get('content', '')
        content = html.unescape(content)
        content = re.sub(r'<[^>]*>', '', content)
        issuer_code = data['issuer']['code']
        whole_name = data['issuer']['localizedTerms'][0]['displayName']
        description = data['layout']['description']
        published_date = data['publishedDate'].split("T")[0]

        if 'this is automaticaly generated document'.lower() in content.lower() or "For more information contact".lower() in content.lower():
            return

        attachments = data.get('attachments', [])
        if attachments:
            att_id = attachments[0].get('attachmentId')
            file_name = attachments[0].get('fileName')

            if file_name.lower().endswith('.pdf'):
                attachment_url = f"https://api.seinet.com.mk/public/documents/attachment/{att_id}"
                response = requests.get(attachment_url)
                if response.status_code == 200:
                    pdf_file = BytesIO(response.content)
                    with pdfplumber.open(pdf_file) as pdf:
                        if pdf.pages:
                            pdf_text = pdf.pages[0].extract_text()
                content += "\n"
                content += pdf_text

        with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                document_id, published_date, description, content, issuer_code, whole_name
            ])
        print(f"Saved document {document_id} to CSV.")
    except Exception as e:
        print(f"Error processing document {document_id}: {e}")


def get_page_data(page):
    start_date = "2022-01-01T00:00:00"
    end_date = datetime.now().strftime("%Y-%m-%dT23:59:59")
    payload = {
        "issuerId": 0,  # 0 => for all Issuers
        "languageId": 2,  # English
        "channelId": 1,  # taking data from Web Page
        "dateFrom": start_date,
        "dateTo": end_date,
        "isPushRequest": False,
        "page": page
    }
    headers = {"Content-Type": "application/json"}
    url = "https://api.seinet.com.mk/public/documents"

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        data = json_data.get('data', [])
        return data
    else:
        print(f"Failed to fetch page {page}: {response.status_code}")
        return []


def retrieve_data():
    if os.path.exists(CSV_FILE_PATH):
        print(f"The file '{CSV_FILE_PATH}' already exists.")
        user_input = input("Do you want to delete it and start again? (yes/no): ").strip().lower()
        if user_input == "yes":
            os.remove(CSV_FILE_PATH)
            print(f"File '{CSV_FILE_PATH}' deleted. Starting data retrieval...")
        else:
            print("Aborting data retrieval.")
            return

    with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'Document_id', 'Date', 'Description', 'Content', 'Company_code', 'Company_whole_name'
        ])

    page = 1
    all_data = []

    while True:
        print(f"Fetching page {page}...")
        page_data = get_page_data(page)
        if not page_data:
            print("No more pages to fetch.")
            break
        all_data.extend(page_data)
        page += 1

    with Pool(processes=8) as pool:
        pool.map(process_news, all_data)


# Example usage
if __name__ == "__main__":
    retrieve_data()

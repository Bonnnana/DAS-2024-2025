import os
import pandas as pd
from transformers import pipeline
import json


def analyze_sentiment_batch(content_list, classifier):
    results = []
    for content in content_list:
        try:
            result = classifier(content, truncation=True, max_length=512)
            results.append(result[0]['label'])
        except Exception as e:
            print(f"Error processing content: {content[:50]}... | Error: {e}")
            continue  # Skip this content and move to the next
    return results


def process_data_in_batches(input_file, classifier_model, output_file, batch_size=32):
    if os.path.exists(output_file):
        print(f"{output_file} already exists. Skipping sentiment analysis because it is already done.")
        return pd.read_csv(output_file)

    data = pd.read_csv(input_file)
    data = data.dropna(subset=['Content'], axis=0).copy()
    data['Content'] = data['Content'].astype(str)
    data = data[data['Content'].str.strip() != ""]  # Remove rows with whitespace-only content

    classifier = pipeline("sentiment-analysis", model=classifier_model, truncation=True, max_length=512)

    sentiments = []
    for i in range(0, len(data), batch_size):
        batch = data['Content'][i:i + batch_size].tolist()
        sentiments.extend(analyze_sentiment_batch(batch, classifier))

    data['Sentiment'] = sentiments

    data.to_csv(output_file, index=False)
    return data


def get_company_signal_with_percentages(sentiment_data, company_code):
    company_data = sentiment_data[sentiment_data['Company_code'] == company_code]

    if company_data.empty:
        return f"No data found for company code: {company_code}"

    # Extract the 'Sentiment' column for the company's data
    sentiments = company_data['Sentiment']

    counts = sentiments.value_counts()
    positive = counts.get("Positive", 0)
    negative = counts.get("Negative", 0)
    neutral = counts.get("Neutral", 0)
    total = sentiments.size

    # If there are no sentiments, return a message
    if total == 0:
        return f"No sentiment data available for company code: {company_code}"

    positive_percentage = (positive / total) * 100
    negative_percentage = (negative / total) * 100
    neutral_percentage = (neutral / total) * 100

    if positive_percentage > 60:
        signal = "Buy"
    elif negative_percentage > 60:
        signal = "Sell"
    else:
        signal = "Hold"

    return {
        "Company": company_code,
        "Positive Percentage": round(positive_percentage, 2),
        "Negative Percentage": round(negative_percentage, 2),
        "Neutral Percentage": round(neutral_percentage, 2),
        "Signal": signal
    }


def get_fundamental_analysis(company_code):
    """
        Function to perform fundamental analysis based on sentiment analysis of company news.

        Args:
            company_code (str): The code of the company to analyze.

        Returns:
            dict: A dictionary containing sentiment percentages (positive, negative, neutral) and the resulting signal (Buy, Sell, or Hold) for the company.
    """
    news_data = "news_data.csv"

    news_sentiment_data = "news_sentiment_data.csv"
    classifier_model = "yiyanghkust/finbert-tone"

    sentiment_data = process_data_in_batches(news_data, classifier_model, news_sentiment_data)

    result = get_company_signal_with_percentages(sentiment_data, company_code)

    return json.dumps(result, indent=4)


# Example usage
# if __name__ == "__main__":
#     print(get_fundamental_analysis("KMB"))